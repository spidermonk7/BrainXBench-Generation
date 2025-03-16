import requests
import json

# 查询 Internet Archive，获取开放书籍的可用格式
def fetch_book_text(query, max_results=5):
    search_url = "https://archive.org/advancedsearch.php"
    params = {
        'q': query,
        'fl[]': 'identifier,title,creator,year,language',
        'sort': 'year desc',
        'rows': max_results,
        'output': 'json'
    }
    
    response = requests.get(search_url, params=params)
    response.raise_for_status()
    data = response.json()

    books = []
    for doc in data['response']['docs']:
        book_id = doc['identifier']
        book = {
            'Title': doc.get('title', 'N/A'),
            'Author': doc.get('creator', 'N/A'),
            'Year': doc.get('year', 'N/A'),
            'Language': doc.get('language', 'N/A'),
            'TXT URL': f"https://archive.org/download/{book_id}/{book_id}.txt",  # 纯文本版本
            'XML URL': f"https://archive.org/download/{book_id}/{book_id}_djvu.xml",  # OCR XML 版本
            'PDF URL': f"https://archive.org/download/{book_id}/{book_id}.pdf"  # PDF 版本
        }
        books.append(book)

    return books

import requests

# 统一的下载函数（适用于 TXT/XML）
def download_book_text(url, filename, file_type="text"):
    """
    通用的文本文件下载器，适用于 TXT 和 XML。
    """
    try:
        response = requests.get(url, stream=True, timeout=10)
        if response.status_code == 200:
            with open(filename, 'w', encoding='utf-8') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # 避免写入空块
                        f.write(chunk.decode('utf-8', errors='ignore'))  # 处理可能的解码错误
            print(f"✅ {file_type.upper()} 书籍下载完成: {filename}")
        else:
            print(f"❌ 书籍下载失败（{file_type.upper()}），HTTP 状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 下载失败（{file_type.upper()}）: {e}")


# PDF 下载函数（适用于二进制文件）
def download_book_pdf(url, filename):
    """
    下载 PDF 文件。
    """
    try:
        response = requests.get(url, stream=True, timeout=15)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:  # 避免写入空块
                        f.write(chunk)
            print(f"✅ PDF 书籍下载完成: {filename}")
        else:
            print(f"❌ 书籍下载失败（PDF），HTTP 状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ PDF 下载失败: {e}")


if __name__ == "__main__":
    # 获取神经科学相关的书籍 TXT 版本
    books = fetch_book_text("neuroscience", max_results=5)
    for idx, book in enumerate(books, 1):
        print(f"Book {idx}:")
        print(f"Title: {book['Title']}")
        print(f"Author: {book['Author']}")
        print(f"Year: {book['Year']}")
        print(f"Language: {book['Language']}")
        print(f"TXT URL: {book['TXT URL']}")
        print(f"XML URL: {book['XML URL']}")
        print(f"🤖: Downloading from link: {book['PDF URL']}")
        # download_book_text(book['TXT URL'], f"{book['Title']}.txt")
        download_book_pdf(book['PDF URL'], f"{book['Title']}.pdf")
        print('-' * 80)
