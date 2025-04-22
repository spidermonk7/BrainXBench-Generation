
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
load_dotenv(override=True)
import json
import seaborn as sns
from tqdm import tqdm

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
    (1) txt_files: a list of texts.
    """
    txt_files = []
    for file in os.listdir(path):
        if file.endswith(".txt"):
            with open(f"{path}/{file}", "r") as f:
                txt_files.append(f.read())

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
 


def check_correlation():
    train_set = load_csv(f"Benches/segmentation/final/csvs/BrainXBench_TF_3K.csv")
    train_abss = []
    for abs in train_set:
        if abs['answer'] == 'text 1':
            abstract_ori = abs['background'] + ' ' + abs['method'] + ' ' + abs['conclusion1']
        elif abs['answer'] == 'text 2':
            abstract_ori = abs['background'] + ' ' + abs['method'] + ' ' + abs['conclusion2']
        else:
            raise ValueError("Invalid answer value")
        
        train_abss.append(abstract_ori)

    oscillations = {}
    
    for year in tqdm(range(17, 25), desc="Checking for oscillations", total= 8):
        # load test set from json file
        test_set = json.load(open(f"workspaces/BrainX-{year}JFM/bench/forward/jsons/Multi_Choice.json"))
        # test_set = json.load(open(f"workspaces/BrainX-17JFM/bench/forward/jsons/Multi_Choice.json"))
        test_abss = []
        for abs in test_set:
            abstract_ori_test = abs[abs['label']]
            if abstract_ori_test in train_abss:
                print(f"Duplicate abstract found in train set: {abstract_ori_test}")
                if year in oscillations:
                    oscillations[year] += 1
                else:
                    oscillations[year] = 1
            else:
                continue
        
    for year in range(17, 25):
        if year not in oscillations:
            oscillations[year] = 0
    
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 6))
    plt.bar(oscillations.keys(), oscillations.values())
    plt.xlabel('Year')
    plt.ylabel('Number of oscillations')
    plt.title('Oscillations in BrainXBench')
    plt.xticks(list(oscillations.keys()))
    plt.grid(axis='y')
    plt.savefig(f"BrainX-oscillations.png", transparent=True, dpi=300)
    plt.show()
    print(f"✅: Successfully saved the oscillations figure.")



LABEL_MATCHING_DIC = {
    "Nature communications": "NC",
    "The Journal of neuroscience : the official journal of the Society for Neuroscience": "JNeurosci",
    "Proceedings of the National Academy of Sciences of the United States of America": "PNAS",
    "Science advances": "Sci Adv",
    "Neuron": "Neuron",
    "Cell reports": "Cell Rep",
    "eLife": "eLife",
    "Alzheimer's & dementia : the journal of the Alzheimer's Association": "Alzheimer",
    "Nature neuroscience": "Nat. Neurosci",
    "The Journal of physiology": "J Physiol"
}

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



import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from collections import defaultdict

def plot_stacked_distribution(data, key, sub_key, plot=False, year = 2024):
    result_dic = defaultdict(lambda: defaultdict(int))

    # 统计每个 key（如 source）内每个 sub_key（如月份）的数量
    for item in data:
        result_dic[item[key]][item[sub_key]] += 1

    if plot:
        plt.style.use('seaborn-v0_8-paper')
        sources = list(result_dic.keys())
        label_sources = sources

        # 可选：映射 source 名（如果你有 LABEL_MATCHING_DIC）
        if key == "Source" and 'LABEL_MATCHING_DIC' in globals():
            label_sources = [LABEL_MATCHING_DIC.get(source, source) for source in sources]

        # 获取所有类别（如 Jan, Feb, Mar）
        pubdates = sorted(set(date for subdict in result_dic.values() for date in subdict.keys()))

        # ✅ 你可以在这里切换配色方案
        color_palette = {
            f"{year}-Jan": "#a6cee3",  # 浅蓝
            f"{year}-Feb": "#b2df8a",  # 浅绿
            f"{year}-Mar": "#a6cee3",  # 粉红
        }
    #     color_palette = {
    #     f"{year}-Jan": "#1b9e77",  # 深绿
    #     f"{year}-Feb": "#d95f02",  # 暗橙
    #     f"{year}-Mar": "#7570b3",  # 深蓝紫
    # }
    #     color_palette = {
    #     f"{year}-Jan": "#4C72B0",  # 深蓝
    #     f"{year}-Feb": "#55A868",  # 青绿
    #     f"{year}-Mar": "#C44E52",  # 深红
    # }


        colors = [color_palette.get(date, "#999999") for date in pubdates]  # fallback 灰色

        # 画布大小
        plt.figure(figsize=(6, 6))

        # 堆叠柱状图
        bottom = np.zeros(len(sources))
        for i, pubdate in enumerate(pubdates):
            values = [result_dic[source].get(pubdate, 0) for source in sources]
            plt.barh(label_sources, values, left=bottom, color=colors[i], label=pubdate)
            bottom += np.array(values)

        # 添加每行末尾总数文字
        for i, source in enumerate(sources):
            total = sum(result_dic[source].values())
            plt.text(total + 0.5, i, str(total), va='center', ha='left', fontsize=10, color='#333333')

        # 美化
        plt.yticks(rotation=0)
        plt.xlabel("Count", fontsize=12)
        plt.ylabel(key.capitalize(), fontsize=12)
        plt.grid(axis="x", linestyle="--", alpha=0.3)
        plt.legend(title=sub_key, loc="upper right", frameon=False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['left'].set_visible(False)
        plt.tight_layout()
        # plt.show()
        plt.savefig(f"figs/month_journal_dis_{year}.png", dpi=300, transparent=True)
        plt.close()


    return result_dic



import matplotlib.pyplot as plt
import pandas as pd

def plot_benchmark_by_year(data_dict):
    years = sorted(data_dict.keys(), key=lambda x: int(x))
    types = ["Opposite Outcome", "Factor Misattribution", "Incorrect Causality"]

    rows = []
    for year in years:
        row = {}
        for t in types:
            val = data_dict.get(year, {}).get(t)
            row[t] = len(val) if val is not None else 0
        row["Year"] = f"20{year}"
        rows.append(row)

    df = pd.DataFrame(rows).set_index("Year")

    # 颜色定义
    colors = {
        "Opposite Outcome": "#8da0cb",
        "Factor Misattribution": "#66c2a5",
        "Incorrect Causality": "#fc8d62"
    }

    # 绘图（紧凑：调整 bar 宽度 & bar 的间距）
    plt.style.use('ggplot')
    fig, ax = plt.subplots(figsize=(10, 6))
    bar_width = 0.8  # 默认是 0.8，调小会更“瘦”；调大更“紧凑”

    bottoms = [0] * len(df)
    x = range(len(df))
    for i, t in enumerate(types):
        values = df[t].values
        bars = ax.bar(
            x, values, bar_width, label=t,
            bottom=bottoms, color=colors[t]
        )

        # 每个区块加上数量标注
        for j, bar in enumerate(bars):
            height = bar.get_height()
            if height > 0:
                ax.text(
                    bar.get_x() + bar.get_width() / 2,  # 中心对齐
                    bar.get_y() + height / 2,           # 垂直居中
                    str(int(height)),
                    ha='center', va='center',
                    fontsize=9, color='white'
                )
        # 更新累计底部
        bottoms = [bottoms[j] + values[j] for j in range(len(values))]

    ax.set_xticks(x)
    ax.set_xticklabels(df.index, rotation=45)
    ax.set_ylabel("Benchmark Size")
    # ax.legend(title="Error Type")
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    plt.tight_layout()
    # plt.show()
    plt.savefig(f"figs/benchmark_by_year.png", dpi=300, transparent=True)


def run_month_journal_distribution():
    for year in range(17, 26):
        if year == 25:
            data = load_csv(f"Benches/forward/flip/csvs/valids_v_direct0.6.csv")
        else:
            data = load_csv(f"workspaces/BrainX-{year}JFM/data/forward/validate/validate_data.csv")
        year = f"20{year}"
        plot_stacked_distribution(data, "Source", "Published Date", plot=True, year=year)

import os
import shutil

def copy_selected_csv_files(source_dir: str, target_dir: str):
    """
    复制 source_dir 中文件名包含指定关键词的 CSV 文件到 target_dir。

    匹配关键词：
    - "Factor_Misattribution"
    - "Opposite_Outcome"
    - "Incorrect_Causal_Relationship"
    """
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)

    keywords = [
        "Factor_Misattribution",
        "Opposite_Outcome",
        "Incorrect_Causal_Relationship"
    ]

    matched_files = [
        f for f in os.listdir(source_dir)
        if f.endswith(".csv") and any(kw in f for kw in keywords)
    ]

    for filename in matched_files:
        src_path = os.path.join(source_dir, filename)
        dst_path = os.path.join(target_dir, filename)
        shutil.copy2(src_path, dst_path)
        print(f"✅ Copied: {filename}")

    print(f"🎉 Done. {len(matched_files)} files copied to {target_dir}")


if __name__ == '__main__':
    # build benchdic
    # bench_dics = {}
    # for year in range(17, 26):
    #     bench_dics[f'{year}'] = {'Opposite Outcome': None, 'Factor Misattribution': None, 'Incorrect Causality': None}
    # # load data
    #     if year != 25:
    #         data_f = load_csv(f"workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Factor_Misattribution-V0.6.csv")
    #         data_o = load_csv(f"workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Opposite_Outcome-V0.6.csv")
    #         data_i = load_csv(f"workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Incorrect_Causal_Relationship-V0.6.csv")
    #     elif year == 25:
    #         data_o = load_csv(f"Benches/forward/final/csvs/Opposite_Outcome-V0.6.csv")
    #         data_f = load_csv(f"Benches/forward/final/csvs/Factor_Misattribution-V0.6.csv")
    #         data_i = load_csv(f"Benches/forward/final/csvs/Incorrect_Causal_Relationship-V0.6.csv")
    #     bench_dics[f'{year}']['Opposite Outcome'] = data_o
    #     bench_dics[f'{year}']['Factor Misattribution'] = data_f
    #     bench_dics[f'{year}']['Incorrect Causality'] = data_i
        
    # # plot the benchmark by year

    # plot_benchmark_by_year(bench_dics)
    AREA_DICT = [
        'hippocampus', 
        'Prefrontal-Cortex', 
        'Striatum', 
        'Cerebellum', 
        'Amygdala'
    ]

    for brain_area in AREA_DICT:
        source_dir = f"workspaces/{brain_area}/bench/forward/csvs"
        target_dir = "/Users/cuishaoyang/Desktop/PKU/KaiTeam/BrainX-NeuroBench/BenchData/BXB/forward/csvs"

        copy_selected_csv_files(source_dir, target_dir)
            

    