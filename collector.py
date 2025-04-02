import os
import time
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from utils import *
from omegaconf import OmegaConf

# 读取配置
cfg = OmegaConf.load("configs/forward_config.yaml")


JOURNAL_WHITELIST = set(cfg.JOURNALS)  # 你可以在 config.yaml 里定义 JOURNALS

def build_pubmed_query(base_term, start_year=None, start_month=None,
                       end_year=None, end_month=None, journals=None):
    """
    构造 PubMed 查询语句，可支持关键词、时间范围（精确到月）、期刊限制。

    Args:
        base_term (str): 搜索关键词，如 "neuroscience"
        start_year (int): 起始年
        start_month (int): 起始月（1-12）
        end_year (int): 结束年
        end_month (int): 结束月（1-12）
        journals (list[str]): 期刊名列表，如 ["Neuron", "eLife"]

    Returns:
        str: 拼接好的 PubMed 查询语句
    """
    query_parts = [base_term]

    # 日期范围
    if start_year and end_year and start_month and end_month:
        start_date = f"{start_year}/{start_month:02d}/01"
        end_date = f"{end_year}/{end_month:02d}/31"  # 最宽松处理月底
        date_filter = f'("{start_date}"[PDAT] : "{end_date}"[PDAT])'
        query_parts.append(date_filter)

    # 期刊限制
    if journals:
        journal_filter = " OR ".join([f'"{j}"[Journal]' for j in journals])
        query_parts.append(f"({journal_filter})")

    return " AND ".join(query_parts)



def fetch_pmid_list(query, max_results, db="pubmed"):
    search_url = f"{cfg.BASE_URL}esearch.fcgi"
    params = {
        "db": db,
        "term": query,
        "retmax": max_results,
        "usehistory": "y",
        "retmode": "xml",
        "api_key": os.getenv("NCBI_API_KEY")
        
    }
    
    response = requests.get(search_url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    web_env = root.find(".//WebEnv").text
    query_key = root.find(".//QueryKey").text
    pmid_list = [id.text for id in root.findall(".//Id")]

    return pmid_list, web_env, query_key

def robust_request(url, params, max_retries=3, backoff=2):
    for i in range(max_retries):
        response = requests.get(url, params=params)
        if response.status_code == 429:
            wait = backoff * (i + 1)
            print(f"⚠️ 429 Too Many Requests. Sleeping {wait}s before retry...")
            time.sleep(wait)
            continue
        response.raise_for_status()
        return response
    raise Exception("Too many 429 errors. Giving up.")


def fetch_article_details(query, pmid_list, web_env, query_key, start_index, batch_size, db="pubmed", thread_id=0, bench_name = "BrainX-v1"):
    try:
        details_url = f"{cfg.BASE_URL}efetch.fcgi"
        batch_ids = pmid_list[start_index:start_index + batch_size]
        params = {
            "db": db,
            "retmode": "xml",
            "WebEnv": web_env,
            "query_key": query_key,
            "id": ",".join(batch_ids), 
            "api_key": os.getenv("NCBI_API_KEY")
        }


        print(f"🌐 Thread-{thread_id} fetching {len(batch_ids)} articles [{start_index} to {start_index + batch_size}]")
        response = robust_request(details_url, params)
        root = ET.fromstring(response.content)

        articles = []
        for pubmed_article in tqdm(root.findall(".//PubmedArticle"), desc=f"Processing articles {start_index + 1} to {start_index + len(batch_ids)}", total=len(batch_ids)):
            article = {}
            try:
                article["Title"] = pubmed_article.find(".//ArticleTitle").text or "N/A"
            except:
                article["Title"] = "N/A"
            try:
                abstract = pubmed_article.find(".//Abstract")
                article["Abstract"] = " ".join([p.text for p in abstract.findall(".//AbstractText")]) if abstract is not None else "N/A"
            except:
                article["Abstract"] = "N/A"
            try:
                doi = pubmed_article.find(".//ArticleId[@IdType='doi']")
                article["DOI"] = doi.text if doi is not None else "N/A"
            except:
                article["DOI"] = "N/A"
            try:
                authors = []
                for author in pubmed_article.findall(".//Author"):
                    last_name = author.find("LastName")
                    first_name = author.find("ForeName")
                    if last_name is not None and first_name is not None:
                        authors.append(f"{first_name.text} {last_name.text}")
                article["Authors"] = authors if authors else "N/A"
            except:
                article["Authors"] = "N/A"
            try:
                pub_date = pubmed_article.find(".//PubDate")
                year = pub_date.find(".//Year")
                month = pub_date.find(".//Month")
                publish_date = f"{year.text}-{month.text}" if year is not None and month is not None else "N/A"
                article['Published Date'] = publish_date
            except:
                publish_date = "N/A"
                article['Published Date'] = publish_date
            try:
                journal_name = pubmed_article.find(".//Journal").find(".//Title")
                article["Source"] = journal_name.text if journal_name is not None else "N/A"
            except:
                article["Source"] = "N/A"
            try:
                mesh_headings = []
                for mesh_heading in root.findall(".//MeshHeading"):
                    descriptor_name = mesh_heading.find("DescriptorName")
                    if descriptor_name is not None:
                        mesh_headings.append(descriptor_name.text)
                article["MeSH Headings"] = mesh_headings if mesh_headings else "N/A"
            except:
                article["MeSH Headings"] = "N/A"

                # ✅ 筛选逻辑
            if article['Published Date'] not in cfg.DATES_CONSIDERED:
                continue
            if article["Source"] not in cfg.JOURNALS:
                continue

            articles.append(article)

        check_path(f"workspaces/{bench_name}/data/raw_abs")
        save_to_csv(articles, save_path=f"workspaces/{bench_name}/data/raw_abs", name=f"raw_abstracts_worker{thread_id}")
        print(f"✅ Thread-{thread_id} saved {len(articles)} articles that meet the requirements to CSV.")
        return articles

    except Exception as e:
        print(f"❌ Thread-{thread_id} crashed with error: {e}")
        return []


def get_query_documents(query="neuroscience", max_results=10, db="pubmed", threads=5, bench_name="BrainX-v1"):
    query = query.lower()
    query = build_pubmed_query(query, start_year=cfg.start_year, start_month=cfg.start_month,
                               end_year=cfg.end_year, end_month=cfg.end_month, journals=JOURNAL_WHITELIST)

    pmid_list, web_env, query_key = fetch_pmid_list(query, max_results)
    print(f"🤖: Found {len(pmid_list)} articles matching '{query}'.")

    batch_count = len(pmid_list) // cfg.PUB_BATCH_SIZE + (1 if len(pmid_list) % cfg.PUB_BATCH_SIZE != 0 else 0)
    futures = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(batch_count):
            start_idx = i * cfg.PUB_BATCH_SIZE
            if start_idx >= len(pmid_list):
                print(f"⚠️ Skipping Thread-{i}, out of range.")
                continue
            futures.append(
                executor.submit(fetch_article_details, query, pmid_list, web_env, query_key,
                                start_idx, cfg.PUB_BATCH_SIZE, db=db, thread_id=i, bench_name=bench_name)
            )

        for i, future in enumerate(futures):
            try:
                future.result()
            except Exception as e:
                print(f"❌ Future {i} failed with error: {e}")



def combine_data_files(folder_path = "data/neuroscience/pubmed"):
    csv_files = [f for f in os.listdir(folder_path) if f.endswith(".csv")]
    print(f"📂 Found {len(csv_files)} CSV files in {folder_path}"
          f"\n🔍 Combining data from all files...")
    combined_data = []
    for file in csv_files:
        combined_data += load_csv(folder_path + '/' + file)

    print(f"🤖: GOT {len(combined_data)} abstracts on the internet.")
    save_to_csv(combined_data, save_path=folder_path, name="combined_abstracts")



if __name__ == "__main__":
    
    get_query_documents(
        query=cfg.query,
        max_results=cfg.max_results,
        db=cfg.db,
        threads=cfg.threads, 
        bench_name=cfg.bench_name
    )

    combine_data_files(folder_path=f"workspaces/{cfg.bench_name}/data/raw_abs")
