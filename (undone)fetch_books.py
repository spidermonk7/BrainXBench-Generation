import requests
import json

# 替换为你自己从Springer开发者平台获取的API密钥
API_KEY = '3e447332d8e9177e20886f510d02a885'
BASE_URL = "https://api.springer.com/metadata/json"

# 获取书籍信息
def fetch_books(query, max_results=1):
    params = {
        'q': query,  # 书籍的查询关键词，如 "neuroscience"
        'api_key': API_KEY,
        'start': 0,  # 从第一个开始
        'rows': max_results,  # 获取的最大书籍数量
        'facet-content-type': 'Book',  # 限定为书籍

        
    }

    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()

    # 解析返回的JSON数据
    data = response.json()

    books = []
    for doc in data['records']:
        print(doc)
        exit()
        book = {}
        book['Title'] = doc.get('title', 'N/A')
        book['DOI'] = doc.get('doi', 'N/A')
        book['Authors'] = [author['name'] for author in doc.get('author', [])]
        book['Publisher'] = doc.get('publisher', 'N/A')
        book['Publication Date'] = doc.get('publicationDate', 'N/A')
        book['URL'] = doc.get('url', 'N/A')
        # get the chapters of the book
        book['Chapters'] = doc.get('chapters', 'N/A')

        books.append(book)

    return books

# 获取神经科学相关的开放获取书籍
books = fetch_books('neuroscience', max_results=1)
for idx, book in enumerate(books, 1):
    print(f"Book {idx}:")
    print(f"Title: {book['Title']}")
    print(f"DOI: {book['DOI']}")
    print(f"Authors: {', '.join(book['Authors'])}")
    print(f"Publisher: {book['Publisher']}")
    print(f"Publication Date: {book['Publication Date']}")
    print(f"URL: {book['URL']}")
    print(f"Chapters: {book['Chapters']}")
    print('-' * 80)
