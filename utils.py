
import os
import numpy as np
import csv
import fitz  # PyMuPDF
from jinja2 import Template
from matplotlib import pyplot as plt
import time
from contextlib import contextmanager
import pandas as pd
from infos import *
from collections import defaultdict
import openai
from dotenv import load_dotenv
load_dotenv()


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

@contextmanager
def timer(name="Execution Time"):
    start_time = time.time()  # 记录开始时间
    yield  # 运行 with 语句内部的代码
    end_time = time.time()  # 记录结束时间
    print(f"⏳ {name}: {end_time - start_time:.4f} 秒")


def load_csv(path):
    """
    Function for loading the csv info
    Require: 
    (1) csv path

    Return:
    (1) A list of dictionaries, each dictionary represents an ITEM, whether it's a paper or a question.
    """
    csv_data = pd.read_csv(path)
    headers = csv_data.columns

    result_dic = []
    for i in range(len(csv_data[headers[0]])):
        item_dic = {}
        for header in headers:
            item_dic[header] = csv_data[header][i]
        result_dic.append(item_dic)
    print(f"📚: Found {len(result_dic)} papers in {path}")
 
    return result_dic


def save_to_csv(dic_list, save_path, name = "v1"):
    """
    Function for saving dict_list to csv file.
    Require:
    (1) dic_list: a list of dictionaries, each dictionary represents an ITEM, whether it's a paper or a question.
    (2) save_path: the path(folder) you want to save the csv file.
    """
    file_name = f"{save_path}/{name}.csv"
    if os.path.exists(file_name):
        with open(file_name, mode='a') as f:
            writer = csv.writer(f)
            for article in dic_list:
                writer.writerow(article.values())
    else:
        with open(file_name, mode='w') as f:
            writer = csv.writer(f)
            writer.writerow(dic_list[0].keys())
            for article in dic_list:
                writer.writerow(article.values())



def load_prompt(path, params):
    with open(path) as f:
        template = Template(f.read())
        prompt = template.render(params)
    return prompt


def LLM_response(model_name = "gpt-4o", prompt = None):
    """
    Function for LLMs generate response directly.
    Require:
    (1) model_name: the model name you want to use.
    (2) prompt: the prompt you want to input.

    Return:
    (1) response: the response from the model, str
    """

    completion = openai.chat.completions.create(
        model=model_name,
        messages=[
            {
                "role": 'user',
                "content": prompt,
            }
        ],
        response_format={'type':"json_object"}
    )
    # print(f"Completion: {completion}")
    anwser = completion.choices[0].message.content
   
    return anwser



def split_and_convert_pdf(input_pdf, output_folder, page_ranges):
    """
    按指定页码范围拆分 PDF，并将拆分后的 PDF 转换为 TXT。
    
    :param input_pdf: 输入 PDF 文件路径
    :param output_folder: 存储拆分后 PDF 和 TXT 文件的文件夹
    :param page_ranges: 页码范围列表，如 [(2,5), (7,19)] 表示 2-5 页为一个文件，7-19 页为另一个文件
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    if type(page_ranges) == int:
        page_ranges = [(i, i + page_ranges) for i in range(49, 1581, page_ranges + 1)]
    # if page_ranges == []:
    #     page_ranges = [(i, i + 2) for i in range(49, 1581, 3)]
    
    # 打开 PDF
    doc = fitz.open(input_pdf)

    for idx, (start_page, end_page) in enumerate(page_ranges):
        # 处理页码（PyMuPDF 的页码从 0 开始，因此要减 1）
        start_page -= 1
        end_page -= 1

        # 创建新 PDF 文档
        new_pdf = fitz.open()
        new_pdf.insert_pdf(doc, from_page=start_page, to_page=end_page)

        # 生成文件名（PDF & TXT）
        pdf_filename = os.path.join(output_folder, f"Chapter_{idx+1}[{start_page+1}-{end_page+1}].pdf")
        txt_filename = os.path.join(output_folder, f"Chapter_{idx+1}_[{start_page+1}-{end_page+1}].txt")

        # 保存拆分的 PDF
        new_pdf.save(pdf_filename)
        new_pdf.close()
        print(f"✅ PDF 拆分完成: {pdf_filename}")

        # 转换 PDF 为 TXT
        convert_pdf_to_text(pdf_filename, txt_filename)

    doc.close()
    print("✅ 所有 PDF 拆分 & 转换 TXT 任务完成！")


def load_txt_files(folder):
    def load_source(path):
        with open(path) as f:
            source = f.read()
        return source
    sources = []
    for f in os.listdir(folder):
        if f.endswith(".txt"):
            sources.append(load_source(os.path.join(folder, f)))
    return sources


def convert_pdf_to_text(input_pdf, output_txt):
    """
    将 PDF 解析为 TXT 文件
    :param input_pdf: PDF 文件路径
    :param output_txt: 输出 TXT 文件路径
    """
    doc = fitz.open(input_pdf)
    with open(output_txt, "w", encoding="utf-8") as f:
        for page_num in range(len(doc)):
            text = doc[page_num].get_text("text")  # 提取纯文本
            f.write(f"===== Page {page_num + 1} =====\n")
            f.write(text + "\n\n")
    
    print(f"✅ PDF 转换为 TXT 完成: {output_txt}")


def pack_data(data_path):
    csv_data = load_csv(data_path)
    df = pd.DataFrame(csv_data)
    path = data_path[:data_path.rfind("/")]
    check_path(path.replace("csv", "parquet"))
    check_path(path.replace("csv", "json"))
    df.to_parquet(data_path.replace("csv", "parquet"), index=False)
    df.to_json(data_path.replace("csv", "json"), orient="records")

    print(f"✅: Successfully saved the data to {data_path.replace('csv', 'parquet')} and {data_path.replace('csv', 'json')}")
 



if __name__ == "__main__":
    input_pdf = PRINCIPLE_NEURAL_SCIENCE_PDF
    output_folder = PRINCIPLE_NEURAL_SCIENCE_PATH + "/chapters/"
    split_and_convert_pdf(input_pdf=input_pdf, output_folder=output_folder, page_ranges=[])

    # raw_abs_ana()
    # check_split_result()