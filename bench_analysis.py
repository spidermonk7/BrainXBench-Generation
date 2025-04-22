import tiktoken
from utils import *
import math
from matplotlib import pyplot as plt
from sentence_transformers import SentenceTransformer
from sklearn.decomposition import PCA
from umap import UMAP
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np



def count_tokens(text, model="gpt-4"):
    # 你可以替换为 "gpt-3.5-turbo", "gpt-4", 或 "gpt-4o"
    enc = tiktoken.encoding_for_model(model)
    tokens = enc.encode(text)
    return len(tokens)



def count_prompt_tokens(path_list:list):
    for path in path_list:
        with open(path, "r") as f:
            text = f.read()
            token_count = count_tokens(text, model="gpt-4")
            print(f"Token count for {path}: {token_count}")


def run_count_prompt():
    path_list = [
        'prompts/forwards/flip.md',
        'prompts/forwards/split.md',
        'prompts/forwards/validation.md',
    ]

    count_prompt_tokens(path_list)


def got_abs_res_len(min=17, max=25):
    """
    Function for getting the length of the abstract and results.
    """
    years = [i for i in range(min, max)]
    dic_lens = {}
    for year in years:
        dic_lens[year] = {'abs':0, 'res':0}
        path = f"workspaces/BrainX-{year}JFM/data/forward/split/split_data.csv"
        file_dics = load_csv(path)
        len_abs = []
        len_res = []
        for dic in file_dics:
            abs = dic['Abstract']
            res = dic['Result']
            
            
            try:
                len_abs.append(count_tokens(abs, model="gpt-4"))
                len_res.append(count_tokens(res, model="gpt-4"))
            except:
                continue
        dic_lens[year]['abs'] = sum(len_abs) / len(len_abs)
        dic_lens[year]['res'] = sum(len_res) / len(len_res) 

    return dic_lens


def got_eta_1(min=17, max = 25):
    years = [i for i in range(min, max)]
    dic_etas = {}
    for year in years:
        dic_etas[year] = {'eta_1':0, 'eta_2':0, 'eta_3O':0, 'eta_3F':0, 'eta_3I':0}
        splits_all = load_csv(f"workspaces/BrainX-{year}JFM/data/forward/split/split_data.csv")
        splits_valid_1 = []
        splits_valid_2 = []
        raw_nums = len(splits_all)
        # Title,Abstract,DOI,Authors,Published Date,Source,MeSH Headings,Background,Method,Result,Intact_or_not,Neuroscience related,Research_or_not

        for item in splits_all:
            if item['Intact_or_not'] == 1 and item['Neuroscience related'] == 1 and item['Research_or_not'] == 1:
                splits_valid_1.append(item)
                if item['Background'] != "" and item['Method'] != "" and item['Result'] != "":
                    splits_valid_2.append(item)
        splits_valid1 = len(splits_valid_1)
        splits_valid2 = len(splits_valid_2)
        dic_etas[year]['eta_1'] = splits_valid1 / raw_nums
        dic_etas[year]['eta_2'] = splits_valid2 / splits_valid1

        raw_valids = len(load_csv(f"workspaces/BrainX-{year}JFM/data/forward/validate/validate_data.csv"))
        O_data = load_csv(f'workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Opposite_Outcome-V0.6.csv')
        F_data = load_csv(f'workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Factor_Misattribution-V0.6.csv')
        I_data = load_csv(f'workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Incorrect_Causal_Relationship-V0.6.csv')

        dic_etas[year]['eta_3O'] = len(O_data) / raw_valids
        dic_etas[year]['eta_3F'] = len(F_data) / raw_valids
        dic_etas[year]['eta_3I'] = len(I_data) / raw_valids

    return dic_etas



def fix_bench_datas():
    # path = 'workspaces/BrainX-19JFM/data/forward/validate/validate_data.csv'
    paths = [
        'workspaces/BrainX-19JFM/bench/forward/csvs/19_Opposite_Outcome-V0.6.csv',
        'workspaces/BrainX-19JFM/bench/forward/csvs/19_Factor_Misattribution-V0.6.csv',
        'workspaces/BrainX-19JFM/bench/forward/csvs/19_Incorrect_Causal_Relationship-V0.6.csv',
    ]


    for path in paths:

        dic = load_csv(path)
        new_dic = []
        exisist_titles = []
        for item in dic:
            if item['Title'] not in exisist_titles:
                exisist_titles.append(item['Title'])
                new_dic.append(item)
            else:
                # with open('workspaces/BrainX-19JFM/data/forward/validate/error.log', 'a') as f:
                #     f.write(f"❌: The {item['Title']} is duplicated.\n")
                continue
        save_path = path.replace(".csv", "")
        check_path(save_path)
        save_to_csv(new_dic, save_path, name = "new")

def estimate_cost():
    len_dics = got_abs_res_len(min=17, max=25)
    prompt_lens = (430 + 930 + 1110)/1000
    gpt_4_inPrice = 2.5/1000
    gpt_4_outPrice = 10/1000
    estimate_costs = {}
    for key in len_dics.keys():
        abs_len = len_dics[key]['abs']/1000
        res_len = len_dics[key]['res']/1000
        
        cost = (prompt_lens + 3*abs_len + 3*res_len) * gpt_4_inPrice + (abs_len + 6*res_len) * gpt_4_outPrice
        print(f"Year {key}: {cost:.4f} USD")
        estimate_costs[key] = cost

    return estimate_costs



def calculate_entropy(min=17, max=25):
    years = [i for i in range(min, max)]
    dic_entropy = {}
    for year in years:
        dic_entropy[year] = {'entropy_O':0, 'entropy_F':0, 'entropy_I':0, 'entropy_multi':0}
        data_o = load_csv(f"workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Opposite_Outcome-V0.6.csv")
        data_f = load_csv(f"workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Factor_Misattribution-V0.6.csv")
        data_i = load_csv(f"workspaces/BrainX-{year}JFM/bench/forward/csvs/{year}_Incorrect_Causal_Relationship-V0.6.csv")
        data_multi = load_csv(f"workspaces/BrainX-{year}JFM/bench/forward/csvs/Multi_Choice.csv")

        choice_count_dic_o = {'text 1':0, 'text 2':0}
        choice_count_dic_f = {'text 1':0, 'text 2':0}
        choice_count_dic_i = {'text 1':0, 'text 2':0}
        choice_count_dic_multi = {'text1':0, 'text2':0, 'text3':0, 'text4':0}

        for bench in [data_o, data_f, data_i, data_multi]:
            for item in bench:
                
                if bench == data_o:
                    print(f"In bench_O, label: {item['label']}")
                    choice_count_dic_o[item['label']] += 1
                elif bench == data_f:
                    print(f"In bench_F, label: {item['label']}")
                    choice_count_dic_f[item['label']] += 1
                elif bench == data_i:
                    print(f"In bench_I, label: {item['label']}")
                    choice_count_dic_i[item['label']] += 1
                elif bench == data_multi:
                    label = item['label'].replace(' ', '')
                    print(f"In bench_multi, label: {label}")
                    choice_count_dic_multi[label] +=1
               
            
        # 计算 Entropy
        def entropy(count_dic):
            total = sum(count_dic.values())
            probs = [count / total for count in count_dic.values()]
            return -sum(p * math.log(p, 2) for p in probs if p > 0)
        
        dic_entropy[year]['entropy_O'] = entropy(choice_count_dic_o)
        dic_entropy[year]['entropy_F'] = entropy(choice_count_dic_f)
        dic_entropy[year]['entropy_I'] = entropy(choice_count_dic_i)
        dic_entropy[year]['entropy_multi'] = entropy(choice_count_dic_multi)

    for key in dic_entropy:
        print(f"Year {key}: entropy_O: {dic_entropy[key]['entropy_O']:.4f}, entropy_F: {dic_entropy[key]['entropy_F']:.4f}, entropy_I: {dic_entropy[key]['entropy_I']:.4f}, entropy_multi: {dic_entropy[key]['entropy_multi']:.4f}")


    # calculate the max entropy of 2 item distribution and 4 item distribution
    max_entropy_2 = -1 * math.log(0.5, 2)
    max_entropy_4 = -1 * math.log(0.25, 2)
    years = list(dic_entropy.keys())
    entropy_o = [dic_entropy[year]['entropy_O'] for year in years]
    entropy_f = [dic_entropy[year]['entropy_F'] for year in years]
    entropy_i = [dic_entropy[year]['entropy_I'] for year in years]
    entropy_multi = [dic_entropy[year]['entropy_multi'] for year in years]

    # Calculate the baseline maximum entropies for 2 items and 4 items
    max_entropy_2 = -1 * math.log(0.5, 2)
    max_entropy_4 = -1 * math.log(0.25, 2)

    # Plotting the entropy values
    plt.style.use('ggplot')
    plt.figure(figsize=(10, 6))
    plt.scatter(years, entropy_o, label="Opposite Outcome", color='#C60033')
    plt.scatter(years, entropy_f, label="Factor Misattribution", color='#2E8B57')
    plt.scatter(years, entropy_i, label="Incorrect Causal Relationship", color='#DAA520')
    plt.scatter(years, entropy_multi, label="Multi Choice", color='#7B68EE')

    # Plot baseline lines for max entropy values
    plt.axhline(max_entropy_2, color='black', linestyle='--', label=f'Max entropy (2 items): {max_entropy_2:.1f}')
    plt.axhline(max_entropy_4, color='grey', linestyle='--', label=f'Max entropy (4 items): {max_entropy_4:.1f}')

    # Labels and title
    plt.xlabel("Year")
    plt.ylabel("Entropy")
    # plt.title("Benchmark Option Distribution Entropy Across Years")
    plt.legend()
    plt.tight_layout()
    # Save the result image
    plt.savefig("figs/benchmark_entropy_distribution.png")
    plt.show()

    return dic_entropy
        
       



# ====== Step 1: 输入你的两组 abstract ======
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from sentence_transformers import SentenceTransformer
import numpy as np

def plot_embed_k_groups(abstract_groups, group_names=None):
    """
    支持K组abstract的embedding可视化。
    
    参数：
        abstract_groups: List[List[str]] - 每组abstract组成的列表
        group_names: List[str] - 可选，每组的标签名
    """

    # ===== Step 1: 拼接所有abstract =====
    all_abstracts = []
    group_sizes = []

    for group in abstract_groups:
        all_abstracts.extend(group)
        group_sizes.append(len(group))
    total_groups = len(abstract_groups) - 1

    # ===== Step 2: 获取embedding =====
    print("🔍 Encoding abstracts...")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    # embeddings = []
    # for abs in tqdm(all_abstracts):
    #     embeddings.append(model.encode(abs))

    embeddings = model.encode(all_abstracts)
    embedding_ref = embeddings[0]

    embeddings = np.abs(embeddings[1:] - embedding_ref)
    
    # embeddings = embeddings[1:]
    # ===== Step 3: t-SNE降维 =====
    print("🌀 Running t-SNE...")
    reducer = TSNE(
        n_components=2,
        # perplexity=30,
        # n_iter=1000,
        # learning_rate='auto',
        # init='pca',
        # random_state=42
    )
    reduced = reducer.fit_transform(embeddings)
    print(f"length of reduced: {len(reduced)}")
    # ===== Step 4: 可视化准备 =====
    color_palette = plt.cm.get_cmap('tab10', total_groups)
    markers = ['o', '^', 's', 'P', 'D', '*', 'X', 'v', '<', '>']  # 最多支持10种

    # ===== Step 5: 绘图 =====
    print("🎨 Plotting...")
    plt.figure(figsize=(10, 8))

    start = 0
    for i in range(total_groups):
        end = start + group_sizes[i]
        group_points = reduced[start:end]

        label = group_names[i] if group_names else f"Group {i+1}"
        color = color_palette(i)
        marker = markers[i % len(markers)]

        plt.scatter(group_points[:, 0], group_points[:, 1],
                    s=50, alpha=0.75, marker=marker,
                    color=color, edgecolor='white', linewidth=0.5,
                    label=label)
        start = end

    # ===== Step 6: 美化图像 =====
    # plt.title("2D t-SNE Embedding of K Abstract Groups", fontsize=18)
    plt.xlabel("Dimension 1", fontsize=13)
    plt.ylabel("Dimension 2", fontsize=13)
    plt.legend(frameon=True, fontsize=12)
    plt.grid(True, linestyle='--', alpha=0.3)
    plt.gca().set_facecolor('#fafafa')
    plt.tight_layout()
    plt.savefig(f"figs/embedding_dis_human_tsne.png")
    plt.show()




if __name__ == "__main__":
    # fix_bench_datas()
    # exit()
    # dic_entropy = calculate_entropy(min=17, max=25)

    data = load_csv("workspaces/BrainX-19JFM/data/forward/validate/validate_data.csv")
    
    data = load_csv("workspaces/BXB/data/forward/validate/validate_data.csv")

    data_human = [d for d in data if d['creator']=='human']
    data_gpt = [d for d in data if d['creator']=='gpt']


    initial_data_human = [d['Abstract'] for d in data_human]
    BB_data_human = [d['incorrect abs'] for d in data_human]
    Opp_FAB = [d['Background'] + ' ' + d['Method'] + ' ' + d['Opposite_Outcome'] for d in data_human]
    Fac_FAB = [d['Background'] + ' ' + d['Method'] + ' ' + d['Factor_Misattribution'] for d in data_human]
    Cau_FAB = [d['Background'] + ' ' + d['Method'] + ' ' + d['Incorrect_Causal_Relationship'] for d in data_human]

    abs_list = [initial_data_human, BB_data_human, Opp_FAB, Fac_FAB, Cau_FAB]

    

    plot_embed_k_groups(abs_list, group_names=['bb-human', 'Opp', 'Fac', 'Cau'])


    # initial_data_gpt = [d['Abstract'] for d in data_gpt]
    # BB_data_gpt = [d['incorrect abs'] for d in data_gpt]
    # Opp_FAB = [d['Background'] + ' ' + d['Method'] + ' ' + d['Opposite_Outcome'] for d in data_gpt]
    # Fac_FAB = [d['Background'] + ' ' + d['Method'] + ' ' + d['Factor_Misattribution'] for d in data_gpt]
    # Cau_FAB = [d['Background'] + ' ' + d['Method'] + ' ' + d['Incorrect_Causal_Relationship'] for d in data_gpt]

    # abs_list = [initial_data_gpt, BB_data_gpt, Opp_FAB, Fac_FAB, Cau_FAB]


    # plot_embed_k_groups(abs_list, group_names=['bb-gpt', 'Opp', 'Fac', 'Cau'])

