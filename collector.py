import requests
import xml.etree.ElementTree as ET
import time
from tqdm import tqdm
from utils_collect import save_to_csv
from concurrent.futures import ThreadPoolExecutor
from infos_collect import *
from argparse import ArgumentParser


def fetch_pmid_list(query, max_results, db="pubmed"):
    search_url = f"{BASE_URL}esearch.fcgi"
    params = {
        "db": db,
        "term": query,
        "retmax": max_results,
        "usehistory": "y",
        "retmode": "xml"
    }
    response = requests.get(search_url, params=params)
    response.raise_for_status() 

    root = ET.fromstring(response.content)
    web_env = root.find(".//WebEnv").text
    query_key = root.find(".//QueryKey").text

    pmid_list = [id.text for id in root.findall(".//Id")]

    return pmid_list, web_env, query_key


def fetch_article_details(pmid_list, web_env, query_key, start_index, batch_size, db="pubmed"):
    details_url = f"{BASE_URL}efetch.fcgi"
    batch_ids = pmid_list[start_index:start_index + batch_size]
    params = {
        "db":  db,
        "retmode": "xml",
        "WebEnv": web_env,
        "query_key": query_key,
        "id": ",".join(batch_ids)
    }
    response = requests.get(details_url, params=params)
    response.raise_for_status()

    root = ET.fromstring(response.content)
    articles = []

    for pubmed_article in tqdm(root.findall(".//PubmedArticle"), desc=f"Processing articles {start_index + 1} to {start_index + len(batch_ids)}", total=len(root.findall(".//PubmedArticle"))):
        article = {}
        try:
            article_title = pubmed_article.find(".//ArticleTitle")
            article["Title"] = article_title.text if article_title is not None else "N/A"
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
            pub_year = pubmed_article.find(".//PubDate").find(".//Year")
            pub_month = pubmed_article.find(".//PubDate").find(".//Month")
            article['Published Date'] = f"{pub_year.text}-{pub_month.text}" if pub_year is not None and pub_month is not None else "N/A"
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
        time.sleep(0.5)  
    
    save_to_csv(articles, save_path=f"data/neuroscience/pubmed/data")

    return articles

def get_query_documents(query="neuroscience", max_results=10, db="pubmed", threads = 5):
    pmid_list, web_env, query_key = fetch_pmid_list(query, max_results)
    print(f"🤖: Found {len(pmid_list)} articles matching '{query}'.")

    articles = []
    batch_count = len(pmid_list) // PUB_BATCH_SIZE + (1 if len(pmid_list) % PUB_BATCH_SIZE != 0 else 0)
    
    with ThreadPoolExecutor(max_workers=threads) as executor:
        futures = []
        for i in range(batch_count):
            futures.append(executor.submit(fetch_article_details, pmid_list, web_env, query_key, i * PUB_BATCH_SIZE, PUB_BATCH_SIZE, db = db))
     
    return articles



if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("--query", type=str, default="neuroscience", help="The query term to search for.")
    args.add_argument("--max_results", type=int, default=10, help="The maximum number of results to fetch.")
    args.add_argument("--db", type=str, default="pubmed", help="The database to search in.")
    args.add_argument("--threads", type=int, default=5, help="The number of threads to use.")
    args.parse_args()


    get_query_documents(
        query=args.query,
        max_results=args.max_results,
        db=args.db, 
        threads = args.threads
    )
