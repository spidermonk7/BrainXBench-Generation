from utils import *
from infos import *
from generate_BrainX import generate_forward
from argparse import ArgumentParser
from omegaconf import OmegaConf
# 读取配置
cfg = OmegaConf.load("configs/config.yaml")





def raw_abs_ana(path, save = True):
    # 加载数据
    """[Function Card]
    Function for analyse the raw abstract data, here we will:
    (1) Check the sources for papers we got. 
    (2) Check their publish date. 
    (3) Filter out the top-10(Selected) Journals with good fame and high quality. 
    """
    abs_data = load_csv(path)
    filtered_data = [item for item in abs_data if item["Source"] in cfg.JOURNALS and item["Published Date"] in cfg.DATES_CONSIDERED and item["Abstract"] != "N/A"]
    
    save_path = path.replace("/combined_abstracts.csv", '').replace("raw_abs", "valid_stage_01")
    check_path(save_path)
    file_name = "selected_data"
    if save:
        if os.path.exists(save_path + f"/{file_name}.csv"):
            print(f"❌: There already exist a file named: {file_name}.csv at location {save_path}, plz check.")
        else:
            save_to_csv(filtered_data, save_path, file_name)
    print(f"📚: Found {len(filtered_data)} papers that should be taken into consideration.")

    return filtered_data


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
            label_sources = [cfg.LABEL_MATCHING_DIC[source] for source in sources]
        
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







def check_abs(abs_data):
    """
    Function for checking the validity of raw abstract data. 
    (1) Check if there is any nan in the data, if so, ignore that item. 
    (2) Save the valid papers to a new csv file.

    """
    # TODO: 
    # (1) The saving logic should be redirected to a new path.
    valids = []
    for _, item in enumerate(abs_data):
        for id, key in enumerate(item.keys()):
            if pd.isna(item[key]):
                print(f"❌: {key} is a nan in the {_}th paper.")
                break
            if id == len(item.keys()) - 1 and item not in valids:
                valids.append(item)
    return valids


def check_split_result(path, save = True):
    """
    Function for checking the split result of the raw data. 
    (1) Check if there is any nan in the data, if so, ignore that item. 
    (2) Save the valid papers to a new csv file.
    """
    data = load_csv(path)
    filter_out_nan = check_abs(data)
    save_path = f"workspaces/{args.bench_name}/data/forward/split"
    check_path(save_path)
    valids = []
    for id, item in enumerate(filter_out_nan):
        if item['Intact_or_not'] == 1 and item['Neuroscience related'] == 1 and item['Research_or_not'] == 1:
            valids.append(item)
        else:
            print(f"❌: The {id}th paper is invalid.")
    if save:
        if os.path.exists(f"workspaces/{args.bench_name}/data/forward/split/split_valids.csv"):
            if input("The file already exists, do you want to overwrite it? (y/n): ") == "y":
                os.remove(f"workspaces/{args.bench_name}/data/forward/split/split_valids.csv")
                save_to_csv(valids, save_path, name = "split_valids")
        else:
            save_to_csv(valids, save_path, name = "split_valids")

    return valids









if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument('-B', "--bench_name", type=str, default="BrainX-v1")
    args = args.parse_args()

    filtered_data = raw_abs_ana(path = f"workspaces/{cfg.bench_name}/data/raw_abs/combined_abstracts.csv", save=True)
    distribution_info = plot_stacked_distribution(filtered_data, "Source", "Published Date", plot=False)
   



    generate_forward('split', 
                    prompt_path='prompts/forwards/split.md',
                    source_path=f'workspaces/{args.bench_name}/data/valid_stage_01/selected_data.csv',
                    save_path=f'workspaces/{args.bench_name}/data/forward/',
                    version=args.bench_name,
                    )
    
    path = f"workspaces/{args.bench_name}/data/forward/split/split_data.csv"
    check_split_result(path=path, save=True)
    print("✅: Split data is validated.")