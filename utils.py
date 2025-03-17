import sys
import os
import numpy as np
# 获取当前脚本的上级目录（即 `BrainX-NeuroBench`）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import csv
import os
import fitz  # PyMuPDF
from jinja2 import Template
from matplotlib import pyplot as plt
import time
from contextlib import contextmanager
import pandas as pd
import os
from infos import *
from collections import defaultdict


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




# def LLM_response(model_name = "gpt-4o-2024-11-20", prompt = None):
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


def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

def split_and_convert_pdf(input_pdf, output_folder, page_ranges):
    """
    按指定页码范围拆分 PDF，并将拆分后的 PDF 转换为 TXT。
    
    :param input_pdf: 输入 PDF 文件路径
    :param output_folder: 存储拆分后 PDF 和 TXT 文件的文件夹
    :param page_ranges: 页码范围列表，如 [(2,5), (7,19)] 表示 2-5 页为一个文件，7-19 页为另一个文件
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)

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

def load_source(path):
    with open(path) as f:
        source = f.read()
    return source

def load_txt_files(folder):
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

def load_prompt(path, params):
    with open(path) as f:
        template = Template(f.read())
        prompt = template.render(params)
    return prompt
   

def check_validation(path, save_path, debug = False):
    """
    Function for Checking the validity of [Background, Method, Result] segmentation. 
    (1) IF there is any nan in the data, ignore that item.
    (2) IF the abstract is not equal to Background + Method + Result, ignore that item.
    (3) Save the valid papers to a new csv file.   
    """

    # TODO:
    # (1) The saving logic should be redirected to a new path.

    split_data = load_csv(path)
    result_dic = {"Nan":0, "Valid":0, "Invalid":0}
    valid_list = []

    for i, item in enumerate(split_data):
        if pd.isna(item["Result"]) or pd.isna(item["Background"]) or pd.isna(item["Method"]):
            print(f"❌: There is a nan in the {i}th paper's segmentation result.")
            result_dic["Nan"] += 1
            continue
        if item['Abstract'].replace(" ", "").replace("\'", "").replace("\"","").lower() != (item["Background"] + item["Method"] + item["Result"]).replace(" ", "").replace("\'", "").replace("\"", "").lower():
            print(f"❌: Abstract is not equal to Background + Method + Results in the {i}th paper.")
            if debug:
                print(f"Abstract: {item['Abstract']}")
                print(f"SUM: {item['Background'] + item['Method'] + item['Result']}")
            result_dic["Invalid"] += 1
            continue
        result_dic["Valid"] += 1
        valid_list.append(item)
        print(f"✅: The {i}th paper is valid.")

    print(f"📚: Found {result_dic['Valid']} valid papers in {path}, valid rate {result_dic['Valid']/len(split_data)}")
    save_to_csv(valid_list, save_path, name = "v2_valids_sum")
    
def check_abs(path, save_path):
    """
    Function for checking the validity of raw abstract data. 
    (1) Check if there is any nan in the data, if so, ignore that item. 
    (2) Save the valid papers to a new csv file.

    """
    # TODO: 
    # (1) The saving logic should be redirected to a new path.
    valids = []
    abs_data = load_csv(path)
    for _, item in enumerate(abs_data):
        for id, key in enumerate(item.keys()):
            if pd.isna(item[key]):
                print(f"❌: {key} is a nan in the {_}th paper.")
                break
            if id == len(item.keys()) - 1 and item not in valids:
                valids.append(item)
    
    save_to_csv(valids, save_path, name = "valids")
    print(f"📚: Found {len(valids)} invalid papers in {path}, valids rate {len(valids)/len(abs_data)}")
    
def raw_abs_ana(path="data/pubmed/valids.csv", plot = False, save = False):
    # 加载数据
    """[Function Card]
    Function for analyse the raw abstract data, here we will:
    (1) Check the sources for papers we got. 
    (2) Check their publish date. 
    (3) Filter out the top-10(Selected) Journals with good fame and high quality. 
    """
    # TODO:
    # (1) Optimize the return structure, return all the infos we want. 
    # (2) Implement the logic for image plotting and saving
    # (3) The "Selected Journal Filter" saving path shoule be re-direct.

    DATES_CONSIDERED = ["2025-Feb", "2025-Mar"]
    abs_data = load_csv(path)

    filtered_data = [item for item in abs_data if item["Source"] in JOURNALS and item["Published Date"] in DATES_CONSIDERED]
   

    distribution_info = plot_stacked_distribution(filtered_data, "Source", "Published Date", plot=plot)

    save_path = "data/pubmed"
    file_name = "selected_data"
    if save:
        if os.path.exists(save_path):
            print(f"❌: There already exist a file named: {file_name} at location {save_path}, plz check.")
        else:
            save_to_csv(filtered_data, save_path, name = "selected_data")
    print(f"📚: Found {len(filtered_data)} papers that should be taken into consideration.")

    return filtered_data, distribution_info



def plot_distribution(data, key, plot= False):
    result_dic = {}
    for item in data:
        if item[key] in result_dic:
            result_dic[item[key]] += 1
        else:
            result_dic[item[key]] = 1

    if plot:
        plt.style.use('ggplot')
        color_range = np.linspace(0.3, 0.8, len(result_dic))  # 让颜色在 0.3~0.8 之间变化
        colors = [plt.cm.Greys(c) for c in color_range]
        width = 5 * len(result_dic)
        plt.figure(figsize=(width, 5))
        plt.bar(result_dic.keys(), result_dic.values(), color=colors,)
        for i, keyy in enumerate(result_dic.keys()):
            plt.text(i, result_dic[keyy] + 1, result_dic[keyy], ha='center', va='bottom')

        plt.xticks([])
        print(f"source_dic: {result_dic.keys()}")
        plt.tight_layout()
        plt.savefig(f"raw_dis_{key}.png", transparent=True)
        plt.show()
        plt.close()

    return result_dic


def plot_stacked_distribution(data, key, sub_key, plot=False):
    result_dic = defaultdict(lambda: defaultdict(int))

   
    # 计算每个 source 内部不同 pubdate 的数量
    for item in data:
        result_dic[item[key]][item[sub_key]] += 1

    if plot:
        plt.style.use('ggplot')
        # 获取不同的 source 和它们对应的 pubdate
        sources = list(result_dic.keys())
        label_sources = sources
        if key == "Source":
            label_sources = [LABEL_MATCHING_DIC[source] for source in sources]
        
        pubdates = sorted(set(date for subdict in result_dic.values() for date in subdict.keys()))
        # 颜色分配
        color_range = np.linspace(0.3, 0.8, len(pubdates))  
        colors = [plt.cm.Greys(c) for c in color_range]

        # 画布大小
        plt.figure(figsize=(10, 8))
        
        # 绘制堆叠柱状图（水平）
        bottom = np.zeros(len(sources))  # 用于累计每个 source 的 bar 左侧起点
        for i, pubdate in enumerate(pubdates):
            values = [result_dic[source].get(pubdate, 0) for source in sources]
            plt.barh(label_sources, values, left=bottom, color=colors[i], label=pubdate)
            bottom += np.array(values)

        # 添加标签
        for i, source in enumerate(sources):
            total = sum(result_dic[source].values())
            plt.text(total + 1, i, total, va='center', ha='left')

        plt.yticks(rotation=0)
        plt.xlabel("Count")
        plt.ylabel(key.capitalize())
        plt.legend(title=sub_key, loc="upper right")
        plt.tight_layout()
        plt.show()
        plt.close()

    return result_dic


def check_split_result(path = "Benches/forward/split/v_direct2.0.csv", save = True):
    """
    Function for checking the split result of the raw data. 
    (1) Check if there is any nan in the data, if so, ignore that item. 
    (2) Save the valid papers to a new csv file.
    """
    data = load_csv(path)
    valids = []
    for item in data:
        if item['Intact_or_not'] == 1 and item['Neuroscience related'] == 1 and item['Research_or_not'] == 1:
            valids.append(item)
        else:
            print(f"❌: The {item}th paper is invalid.")
    if save:
        save_path = "Benches/forward/split"
        check_path(save_path)
        save_to_csv(valids, save_path, name = "splited_valids")

    return valids




import json
import re

def parse_json_response(response: str):
    """
    Parses a JSON response string, removing markdown-style ```json wrappers if present.

    Args:
        response (str): The raw response string from LLM.

    Returns:
        dict: The parsed JSON object, or None if parsing fails.
    """
    # response = response.strip()
    # print(f"Initial response")
    # print(f"{response}")
    # print('='*20)
    # # Check if the response is wrapped in a markdown code block
    # if response.startswith("```json") or response.startswith("```"):
    #     response = re.sub(r"^```json\s*", "", response)  # Remove ```json at the start
    #     response = re.sub(r"^```\s*", "", response)  # Remove ``` at the start
    #     response = re.sub(r"\s*```$", "", response)  # Remove ``` at the end
    # print(f"Response after removing markdown")
    # print(f"{response}")
    # print('='*20)

    try:
        return eval(response)
    except Exception as e:
        print(f"❌: Error occurs when parsing response: {response}")
        print(f"❌: Error message: {e}")
        return None


if __name__ == "__main__":
    # input_pdf = PRINCIPLE_NEURAL_SCIENCE_PDF
    # output_folder = PRINCIPLE_NEURAL_SCIENCE_PATH + "/chapters/"
    # split_and_convert_pdf(input_pdf=input_pdf, output_folder=output_folder, page_ranges=PRINCIPLE_NEURAL_SCIENCE_CHAPTERS)

    # raw_abs_ana()
    check_split_result()