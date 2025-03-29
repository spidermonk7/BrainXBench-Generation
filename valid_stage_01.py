from utils import *
from infos import *


def raw_abs_ana(path, save = False):
    # 加载数据
    """[Function Card]
    Function for analyse the raw abstract data, here we will:
    (1) Check the sources for papers we got. 
    (2) Check their publish date. 
    (3) Filter out the top-10(Selected) Journals with good fame and high quality. 
    """
    abs_data = load_csv(path)
    filtered_data = [item for item in abs_data if item["Source"] in JOURNALS and item["Published Date"] in DATES_CONSIDERED and item["Abstract"] != "N/A"]
    
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



if __name__ == "__main__":
    from argparse import ArgumentParser
    args = ArgumentParser()
    args.add_argument('-B', "--bench_name", type=str, default="BrainX-v1")
    args = args.parse_args()

    filtered_data = raw_abs_ana(path = f"workspaces/{args.bench_name}/data/raw_abs/combined_abstracts.csv", save=True)
    distribution_info = plot_stacked_distribution(filtered_data, "Source", "Published Date", plot=False)
    print(distribution_info)
    for key, value in distribution_info.items():
        print(f"Source {key}: {value}")