import os
from utils import *
from omegaconf import OmegaConf
from argparse import ArgumentParser
from tqdm import tqdm
from dotenv import load_dotenv


load_dotenv(override=True)

openai_ENV = os.getenv('OPENAI_API_KEY')
print(f"openai env: {openai_ENV}")
# exit()
# 读取配置
cfg = OmegaConf.load("configs/forward_config.yaml")


def generate_forward(task, 
                    prompt_path, 
                    source_path, 
                    save_path, 
                    model_name = "gpt-4o", 
                    version = "BrainX-v1", 
                    domain="neuroscience"
                    ):
    """
    Function for generating the forward bench, including two steps: Split and Flip.
    
    (1) Split: Segment the abstract into Background, Method, and Results.
    (2) Flip: Modify Method and Results part, offer incorrect choice for model evaluation. 
    (3) Save the results to a new csv file.
    """

    paper_infos = load_csv(source_path)
    save_path = save_path + task
    check_path(save_path)

    if os.path.exists(save_path + f"/{task}_data.csv"):
        last_id = len(load_csv(save_path + f"/{task}_data.csv"))
    else:
        last_id = -1

    for id, paper_info in tqdm(enumerate(paper_infos), desc=f"🤖: Processing abstracts", total = len(paper_infos)):
        if id < last_id: continue
        if task == "split":
            params = {
                "domain": domain,
                "abstract": paper_info["Abstract"],
            }
        elif task == "flip":
            assert "Background" in paper_info.keys() and "Method" in paper_info.keys() and "Result" in paper_info.keys(), "Background, Method, and Results are required in the csv file."
            params = {
                "domain": domain,
                "background": paper_info["Background"],
                "method": paper_info["Method"],
                "results": paper_info["Result"],
            }
        elif task == "validate":
            params = {
            'domain':domain,
            "initial_conclusion": paper_info["Result"],
            "Opposite_Outcome": paper_info["Opposite_Outcome"],
            "Factor_Misattribution": paper_info["Factor_Misattribution"],
            "Incorrect_Causal_Relationship": paper_info["Incorrect_Causal_Relationship"],
            }
        prompt = load_prompt(prompt_path, params)
        # print(f"🤖: Stage is {task}, prompt is {prompt}.")
        try:
            output = LLM_response(prompt=prompt, model_name=model_name)
            response = eval(output.strip())
        except:
            with open(f"{save_path}/error.log", "a") as f:
                f.write(f"Error occurs when processing abstract {id}, program exits.\n")
                f.write(f"Response: {output}")
            raise ValueError(f"Error occurs when processing abstract {id} for bench: {version}.")
        
        for key in response.keys():
            paper_info[key] = response[key]
       
        bench_data = [paper_info]
        save_to_csv(bench_data, save_path, f"{task}_data")



import concurrent.futures
import threading

def generate_forward_multithread(task, 
                                  prompt_path, 
                                  source_path, 
                                  save_path, 
                                  model_name="gpt-4o", 
                                  version = "BrainX-v1",
                                  domain="neuroscience",
                                  max_workers=8):
    paper_infos = load_csv(source_path)
    save_path = save_path + task
    check_path(save_path)

    csv_lock = threading.Lock()  # 🔒用于写入 CSV 时加锁

    if os.path.exists(save_path + f"/{task}_data.csv"):
        last_id = len(load_csv(save_path + f"/{task}_data.csv"))
    else:
        last_id = -1

    def process_single_paper(id, paper_info):
        if id < last_id:
            return

        try:
            if task == "split":
                params = {
                    "domain": domain,
                    "abstract": paper_info["Abstract"],
                }
            elif task == "flip":
                assert "Background" in paper_info and "Method" in paper_info and "Result" in paper_info, \
                    "Background, Method, and Results are required in the csv file."
                params = {
                    "domain": domain,
                    "background": paper_info["Background"],
                    "method": paper_info["Method"],
                    "results": paper_info["Result"],
                }
            elif task == "validate":
                params = {
                    'domain': domain,
                    "initial_conclusion": paper_info["Result"],
                    "Opposite_Outcome": paper_info["Opposite_Outcome"],
                    "Factor_Misattribution": paper_info["Factor_Misattribution"],
                    "Incorrect_Causal_Relationship": paper_info["Incorrect_Causal_Relationship"],
                }

            prompt = load_prompt(prompt_path, params)
            output = LLM_response(prompt=prompt, model_name=model_name)
            response = eval(output.strip())

            for key in response:
                paper_info[key] = response[key]

            with csv_lock:
                save_to_csv([paper_info], save_path, f"{task}_data")

        except Exception as e:
            with open(f"{save_path}/error.log", "a") as f:
                f.write(f"Error on abstract {id}:\n{str(e)}\nResponse: {output}\n")

    with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
        list(tqdm(executor.map(lambda args: process_single_paper(*args), enumerate(paper_infos)),
                  total=len(paper_infos),
                  desc="🤖: Processing in parallel"))




def raw_abs_ana(path, save = True):
    # 加载数据
    """[Function Card]
    Function for analyse the raw abstract data, here we will:
    (1) Check the sources for papers we got. 
    (2) Check their publish date. 
    (3) Filter out the top-10(Selected) Journals with good fame and high quality. 
    """
    abs_data = load_csv(path)
    filtered_data = check_abs(abs_data)
    save_path = path.replace("/combined_abstracts.csv", '').replace("raw_abs", "valid_stage_01")
    check_path(save_path)
    file_name = "selected_data"
    if save:
        if os.path.exists(save_path + f"/{file_name}.csv"):
            if input(f"❓: There already exist a file named: {file_name}.csv at location {save_path}, do you want to overwrite it? (y/n): ") == "y":
                os.remove(save_path + f"/{file_name}.csv")
                save_to_csv(filtered_data, save_path, file_name)
        else:
            save_to_csv(filtered_data, save_path, file_name)
    print(f"🤖: After checking 'N/A's, found {len(filtered_data)} papers that should be taken into consideration.")

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
                # print(f"❌: {key} is a nan in the {_}th paper.")
                # with open(f"workspaces/{cfg.bench_name}/data/raw_abs/error.log", "a") as f:
                #     f.write(f"{key} is a nan in the {_}th paper, DOI: {item['DOI']}.\n")
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
    save_path = f"workspaces/{cfg.bench_name}/data/forward/split"
    check_path(save_path)
    valids = []
    for id, item in enumerate(filter_out_nan):
        if item['Intact_or_not'] == 1 and item['Domain related'] == 1 and item['Research_or_not'] == 1:
            valids.append(item)
        else:
            # with open(f"{save_path}/error.log", "a") as f:
            #     f.write(f"❌: The {id}th paper is not valid for the split data, DOI: {item['DOI']}\n")
            continue
    if save:
        if os.path.exists(f"workspaces/{cfg.bench_name}/data/forward/split/split_valids.csv"):
            if input("The file already exists, do you want to overwrite it? (y/n): ") == "y":
                os.remove(f"workspaces/{cfg.bench_name}/data/forward/split/split_valids.csv")
                save_to_csv(valids, save_path, name = "split_valids")
        else:
            save_to_csv(valids, save_path, name = "split_valids")

    return valids







if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("-S", "--stage", type=str, default="split")
    args.add_argument("-T",'--max_workers', type=int, default=8 )

    args = args.parse_args()
    if args.stage == "S_V_S":
        # filtered_data = raw_abs_ana(path = f"workspaces/{cfg.bench_name}/data/raw_abs/combined_abstracts.csv", save=True)
        # distribution_info = plot_stacked_distribution(filtered_data, "Source", "Published Date", plot=False)
    
        # generate_forward('split', 
        #                 prompt_path='prompts/forwards/split.md',
        #                 source_path=f'workspaces/{cfg.bench_name}/data/valid_stage_01/selected_data.csv',
        #                 save_path=f'workspaces/{cfg.bench_name}/data/forward/',
        #                 version=cfg.bench_name,
        #                 model_name=cfg.segment_model,
        #                 domain = cfg.domain

        #                 )
        generate_forward_multithread('split', 
                        prompt_path='prompts/forwards/split.md',
                        source_path=f'workspaces/{cfg.bench_name}/data/valid_stage_01/selected_data.csv',
                        save_path=f'workspaces/{cfg.bench_name}/data/forward/',
                        version=cfg.bench_name,
                        model_name=cfg.segment_model,
                        domain = cfg.domain,
                        max_workers=args.max_workers

                        )
        
        path = f"workspaces/{cfg.bench_name}/data/forward/split/split_data.csv"
        valids = check_split_result(path=path, save=True)
        print(f"✅: Split data is validated, find in all {len(valids)} valid papers.")

    elif args.stage == "flip":
        # generate_forward('flip', 
        #             prompt_path='prompts/forwards/flip.md',
        #             source_path=f'workspaces/{cfg.bench_name}/data/forward/split/split_valids.csv',
        #             save_path=f'workspaces/{cfg.bench_name}/data/forward/',
        #             version=cfg.bench_name,
        #             model_name=cfg.flip_model,
        #             )
        generate_forward_multithread('flip', 
                    prompt_path='prompts/forwards/flip.md',
                    source_path=f'workspaces/{cfg.bench_name}/data/forward/split/split_valids.csv',
                    save_path=f'workspaces/{cfg.bench_name}/data/forward/',
                    version=cfg.bench_name,
                    model_name=cfg.flip_model,
                    )
        
    elif args.stage == "validate":
    #     generate_forward(
    #     task="validate", 
    #     prompt_path="prompts/forwards/validation.md", 
    #     source_path=f"workspaces/{cfg.bench_name}/data/forward/flip/flip_data.csv",
    #     save_path=f"workspaces/{cfg.bench_name}/data/forward/", 
    #     model_name=cfg.validation_model,
    # )
        generate_forward_multithread(
        task="validate", 
        prompt_path="prompts/forwards/validation.md", 
        source_path=f"workspaces/{cfg.bench_name}/data/forward/flip/flip_data.csv",
        save_path=f"workspaces/{cfg.bench_name}/data/forward/", 
        model_name=cfg.validation_model,
    )

