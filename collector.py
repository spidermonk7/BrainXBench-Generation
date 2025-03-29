import os
import time
import requests
import xml.etree.ElementTree as ET
from tqdm import tqdm
from concurrent.futures import ThreadPoolExecutor
from argparse import ArgumentParser
from utils import save_to_csv, check_path
from infos import *


def fetch_pmid_list(query, max_results, db="pubmed"):
    search_url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": db,
        "term": query,
        "retmax": max_results,
        "usehistory": "y",
        "retmode": "xml",
        "api_key": NCBI_API_KEY
        
    }
    
    response = requests.get(search_url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    web_env = root.find(".//WebEnv").text
    query_key = root.find(".//QueryKey").text
    pmid_list = [id.text for id in root.findall(".//Id")]

    print(f"[DEBUG] Actually got {len(pmid_list)} pmids from esearch.")
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


def fetch_article_details(query, pmid_list, web_env, query_key, start_index, batch_size, db="pubmed", thread_id=0):
    try:
        details_url = f"{BASE_URL}efetch.fcgi"
        batch_ids = pmid_list[start_index:start_index + batch_size]
        params = {
            "db": db,
            "retmode": "xml",
            "WebEnv": web_env,
            "query_key": query_key,
            "id": ",".join(batch_ids), 
            "api_key": NCBI_API_KEY
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
                article['Published Date'] = f"{year.text}-{month.text}" if year is not None and month is not None else "N/A"
            except:
                article['Published Date'] = "N/A"
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

            articles.append(article)

        check_path(f"data/{query}/pubmed/data")
        save_to_csv(articles, save_path=f"data/{query}/pubmed/data", name=f"raw_abstracts_worker{thread_id}")
        print(f"✅ Thread-{thread_id} saved {len(articles)} articles to CSV.")
        return articles

    except Exception as e:
        print(f"❌ Thread-{thread_id} crashed with error: {e}")
        return []


def get_query_documents(query="neuroscience", max_results=10, db="pubmed", threads=5):
    query = query.lower()
    pmid_list, web_env, query_key = fetch_pmid_list(query, max_results)
    print(f"🤖: Found {len(pmid_list)} articles matching '{query}'.")

    batch_count = len(pmid_list) // PUB_BATCH_SIZE + (1 if len(pmid_list) % PUB_BATCH_SIZE != 0 else 0)
    futures = []

    with ThreadPoolExecutor(max_workers=threads) as executor:
        for i in range(batch_count):
            start_idx = i * PUB_BATCH_SIZE
            if start_idx >= len(pmid_list):
                print(f"⚠️ Skipping Thread-{i}, out of range.")
                continue
            futures.append(
                executor.submit(fetch_article_details, query, pmid_list, web_env, query_key,
                                start_idx, PUB_BATCH_SIZE, db=db, thread_id=i)
            )

        for i, future in enumerate(futures):
            try:
                future.result()
            except Exception as e:
                print(f"❌ Future {i} failed with error: {e}")



def combine_data_files(folder_path = ""):
    pass






if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--query", type=str, default="neuroscience", help="The query term to search for.")
    parser.add_argument("--max_results", type=int, default=50, help="The maximum number of results to fetch.")
    parser.add_argument("--db", type=str, default="pubmed", help="The database to search in.")
    parser.add_argument("--threads", type=int, default=5, help="Number of concurrent threads.")

    args = parser.parse_args()

    get_query_documents(
        query=args.query,
        max_results=args.max_results,
        db=args.db,
        threads=args.threads
    )
