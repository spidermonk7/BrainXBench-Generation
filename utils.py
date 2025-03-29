
import os
import numpy as np
import csv
import fitz  # PyMuPDF
from jinja2 import Template
from matplotlib import pyplot as plt
import time
from contextlib import contextmanager
import pandas as pd
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



def load_txt_files(path):
    """
    Function for loading txt files in the given path.
    Require:
    (1) path: the path you want to load txt files.

    Return:
    (1) txt_files: a list of txt files.
    """
    txt_files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            txt_files.append(file)
    return txt_files

def pack_data(data_path):
    csv_data = load_csv(data_path)
    df = pd.DataFrame(csv_data)
    path = data_path[:data_path.rfind("/")]
    check_path(path.replace("csv", "parquet"))
    check_path(path.replace("csv", "json"))
    df.to_parquet(data_path.replace("csv", "parquet"), index=False)
    df.to_json(data_path.replace("csv", "json"), orient="records")

    print(f"✅: Successfully saved the Parquet and JSON file for {data_path}.")
 
