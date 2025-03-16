"""
================================================
File for raw data generating.
From Books to Pretraining Data for LLMs. 
================================================
"""
import os
import json
import pandas as pd
import tiktoken  # 用于按 token 长度切分
import nltk
from .utils import *
from .infos import *
from argparse import ArgumentParser


nltk.download('punkt')

if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("--bookname", type = str, default = "Koch", help = "The book name for the backward bench.")
    args.add_argument("--max_tokens", type = int, default = 512, help = "The maximum number of tokens for each data.")
    args.parse_args()

    book_name = BOOK_INFO_DICT[args.bookname]["Full Name"]
    # 配置
    txt_folder =f"data/books/pdfs/{book_name}/chapters" 
    output_dir = f"data/books/pretrain"
    check_path(output_dir)
    output_jsonl = output_dir + f"/{book_name}.jsonl"
    output_csv = output_dir + f"/{book_name}.csv"

    # 获取所有 txt 文件
    txt_files = sorted([f for f in os.listdir(txt_folder) if f.endswith(".txt")])
    # Tokenizer（GPT-3/4, LLaMA 等适用）
    tokenizer = tiktoken.get_encoding("cl100k_base")  # OpenAI 的 tokenizer

    # 存储数据
    data = []
    # 读取 & 处理文本
    for idx, txt_file in enumerate(txt_files, 1):
        file_path = os.path.join(txt_folder, txt_file)
        
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read().strip()
        # 按 "空行" 分割（段落方式）
        paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
        # 进一步分割成 token 限制的 chunks
        chunk = []
        chunk_token_count = 0
        for para in paragraphs:
            tokens = tokenizer.encode(para)  # 计算当前段落的 token 数
            if chunk_token_count + len(tokens) > args.max_tokens:
                # 存储当前 chunk
                if chunk == []:
                    continue
                data.append({"index": len(data) + 1, "text": " ".join(chunk)})
                chunk = []
                chunk_token_count = 0
            chunk.append(para)
            chunk_token_count += len(tokens)
        # 存储最后的 chunk
        if chunk:
            data.append({"index": len(data) + 1, "text": " ".join(chunk)})
    # 保存为 JSONL
    with open(output_jsonl, "w", encoding="utf-8") as f:
        for entry in data:
            f.write(json.dumps({"text": entry["text"]}, ensure_ascii=False) + "\n")
    # 保存为 CSV
    df = pd.DataFrame(data)
    df.to_csv(output_csv, index=False, encoding="utf-8")
    print(f"🤖: Dataset saved: {output_jsonl}, {output_csv}")
