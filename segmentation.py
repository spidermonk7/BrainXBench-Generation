from datasets import load_dataset
from utils import *


mini = False
def build_segment_bench(mini):
    if mini:
        data = load_dataset("BrainGPT/train_valid_split_pmc_neuroscience_2002-2022_filtered_subset_mini")

    else:
        data = load_dataset("BrainGPT/train_valid_split_pmc_neuroscience_2002-2022_filtered_subset", split = "train[:2%]")    

    # check data length

    return data


import pandas as pd
import os

def split_csv(file_path, output_dir, chunk_size=500):
    """
    将 CSV 文件按指定行数拆分成多个小文件。

    参数：
    - file_path: str，输入 CSV 文件路径
    - output_dir: str，拆分后的文件存放目录
    - chunk_size: int，每个子文件包含的最大行数（默认 1000 行）
    """
    # 确保输出目录存在
    os.makedirs(output_dir, exist_ok=True)

    # 读取 CSV 文件
    df = pd.read_csv(file_path, chunksize=chunk_size)

    # 拆分并保存
    for i, chunk in enumerate(df):
        output_file = os.path.join(output_dir, f"split_{i+1}.csv")
        chunk.to_csv(output_file, index=False)
        print(f"✅ Saved {output_file}")

    print("🚀 CSV 文件拆分完成！")



if __name__ == "__main__":
   
    # mini = False
    # data_split2 = build_segment_bench(mini)
    # print(data_split2)
    # # for i in range(10):
    # #     print(data_split2[i])

    # # calcualte the average length | max length | min length
    
    # # filter out the data with length > 1024

    # data_split2 = [item for item in data_split2 if len(item['text'].split(' ')) <= 256]

    # print(f"size of remaining data: {len(data_split2)}")
    # lengths = [len(item['text'].split(' ')) for item in data_split2]
    # avg_length = sum(lengths) / len(lengths)
    # max_length = max(lengths)
    # min_length = min(lengths)

    # print(f"Average length: {avg_length}")
    # print(f"Max length: {max_length}")
    # print(f"Min length: {min_length}")

    # check_path("Benches/segmentation/csvs")

    # # save the data to csv
    # save_to_csv(data_split2, "Benches/segmentation/csvs", "raw_abs_v1")


    path = "Benches/segmentation/csvs/raw_abs_v1.csv"
    split_csv(path, "Benches/segmentation/csvs/splited_csvs")