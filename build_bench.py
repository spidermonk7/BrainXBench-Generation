from utils import *
from infos import *
import random
from omegaconf import OmegaConf

# 读取配置
cfg = OmegaConf.load("configs/config.yaml")


def load_brainXbench_forward(result_type,file_type = "csv", data_version = 0.6):

    """
    Function for loading brainXbench forward data
    Required:
    (1) The path of the csv file
    (2) Combination of the data: Background, Method, Conclusion

    Return:
    (1) List of dictionary with fake_abstract and true_abstract
    """
    path = f"Benches/forward/final/{file_type}s/{result_type}-V{data_version}.{file_type}"
    bench_data = load_csv(path)

    return bench_data
        

def load_brainXbench_backward(question_type, mini):
    if mini:
        path = f"Benches/backward/BrainXBench_{question_type}_mini.csv"
    else:
        if question_type == "TF":
            raise ValueError("❌: The full version of TF is not available.")
        path = f"Benches/backward/BrainXBench_{question_type}.csv"
    bench_data = load_csv(path)

    return bench_data
    


def build_brainXbench_forward(bench_name = "BrainX-v1"):
    raw_path = f"workspaces/{bench_name}/data/forward/validate/validate_data.csv"
    bench_data = load_csv(raw_path)
    for result_type in ["Opposite_Outcome", "Incorrect_Causal_Relationship", "Factor_Misattribution"]:
        bench_dics = []
        for item in bench_data:
            bench_dic = {}
            fake_abstract = item["Background"] + ' ' + item["Method"] + ' ' + item[result_type]
            # randomly shuffle which goes first
            if random.random() > 0.5:
                bench_dic["text 1"] = item["Abstract"]
                bench_dic["text 2"] = fake_abstract
                bench_dic["label"] = "text 1"
            else:
                bench_dic["text 1"] = fake_abstract
                bench_dic["text 2"] = item["Abstract"]
                bench_dic["label"] = "text 2"

            if item[f"valid: {result_type}"] == 1:
                bench_dics.append(bench_dic)

        save_path = f"workspaces/{bench_name}/bench/forward/csvs"
        check_path(save_path)
       
        if os.path.exists(f"{save_path}/{result_type}.csv"):
            print(f"💁: The file {result_type}.csv already exists.")
            if input(f"💁: Do you want to overwrite it? (y/n)") == "y":
                os.remove(f"{save_path}/{result_type}.csv")
                save_to_csv(bench_dics, save_path, f"{result_type}")
                pack_data(f"{save_path}/{result_type}.csv")
                print(f"✅: Successfully saved the data to {save_path}")
        else:
            save_to_csv(bench_dics, save_path, f"{result_type}")
            pack_data(f"{save_path}/{result_type}.csv")
            print(f"✅: Successfully saved the data to {save_path}")



def build_brainXbench_forward_multi(bench_name = "BrainX-v1"):
    raw_path = f"workspaces/{bench_name}/data/forward/validate/validate_data.csv"
    bench_data = load_csv(raw_path)
    bench_dics = []
    for item in bench_data:
        bench_dic = {}
        fake_abstract1 = item["Background"] + ' ' + item["Method"] + ' ' + item["Opposite_Outcome"]
        fake_abstract2 = item["Background"] + ' ' + item["Method"] + ' ' + item["Incorrect_Causal_Relationship"]
        fake_abstract3 = item["Background"] + ' ' + item["Method"] + ' ' + item["Factor_Misattribution"]
        true_abstract = item["Abstract"]

        # randomly shuffle the orders for multiple choice
        choices = [fake_abstract1, fake_abstract2, fake_abstract3, true_abstract]
        
        random.shuffle(choices)
        
        for i, choice in enumerate(choices):
            bench_dic[f"text{i+1}"] = choice

        label = None
        for key, text in bench_dic.items():
            if bench_dic[key] == true_abstract:
                label = key
                print(f"find the label: {label}")
                break
        bench_dic["label"] = label
        current_dic = bench_dic.copy()

        for key, text in current_dic.items():
            if text == fake_abstract1:
                bench_dic[key + "_type"] = "Opposite_Outcome"
            elif key == "label": continue
            elif text == fake_abstract2:
                bench_dic[key + "_type"] = "Incorrect_Causal_Relationship"
            elif text == fake_abstract3:
                bench_dic[key + "_type"] = "Factor_Misattribution"
            else:
                bench_dic[key + "_type"] = "True"

        
        bench_dics.append(bench_dic)
   
    save_path = f"workspaces/{bench_name}/bench/forward/csvs"
    check_path(save_path)
    save_to_csv(bench_dics, save_path, f"Multi_Choice")
    pack_data(f"{save_path}/Multi_Choice.csv")
    print(f"✅: Successfully saved the data to {save_path}")


def build_brainXbench_backward(raw_path):
    bench_data = load_csv(raw_path)
    
    mini = "_mini" if "mini" in path else ""

    bench_dics = []
    for item in bench_data:
        bench_dic = {}
        descriptionA = item["Description A"]
        descriptionB = item["Description B"]
        judgeA = item["Judgement A"]
        judgeB = item["Judgement B"]

        # randomly shuffle which goes first
        if random.random() > 0.5:
            bench_dic["text 1"] = descriptionA
            bench_dic["text 2"] = descriptionB
            if judgeA == 1:
                bench_dic["label"] = "text 1"
            else:
                bench_dic["label"] = "text 2"

        else:
            bench_dic["text 1"] = descriptionB
            bench_dic["text 2"] = descriptionA
            if judgeB == 1:
                bench_dic["label"] = "text 1"
            else:
                bench_dic["label"] = "text 2"
        bench_dics.append(bench_dic)

    save_path = f"Benches/backward/final/csvs"
    check_path(save_path)

    # check if the file exist
    # if os.path.exists(f"{save_path}/BrainXBench_CHOICE{mini}"):
    #     if input(f"💁: The file BrainXBench_CHOICE{mini}.csv already exists. Do you want to overwrite it? (y/n)") == "y":
    #         os.remove(f"{save_path}/BrainXBench_CHOICE{mini}.csv")
    #         save_to_csv(bench_dics, save_path, f"BrainXBench_CHOICE{mini}")
    #         print(f"✅: Successfully saved the data to {save_path}")
    # else:
    #     save_to_csv(bench_dics, save_path, f"BrainXBench_CHOICE{mini}")

    save_to_csv(bench_dics, save_path, f"BrainXBench_CHOICE")

def build_segment_set(path_folder):
    # load all files in the folder
    data = []
    for file in os.listdir(path_folder):
        if file.endswith(".csv"):
            data += load_csv(f"{path_folder}/{file}")
    data_dics = []
    origin_dics = []
    for id, item in enumerate(data):
        print(f"Item.keys: {item.keys()}")
        data_dic = {}
        if item["Intact_or_not"] != 1:
            print(f"❌ Ignore data {id} because it is not intact.")
            continue
        if item["Research_or_not"] != 1:
            print(f"❌ Ignore data {id} because it is not research related.")
            continue
        if item["Neuroscience related"] != 1:
            print(f"❌ Ignore data {id} because it is not neuroscience related.")
            continue
    
        if item["Abstract"] != str(item["Background"]) + ' ' + str(item["Method"]) + ' ' + str(item["Result"]):
            print(f"❌ Ignore data {id} because the abstract is not the combination of Background, Method, and Result.")
            continue
        # params = {"background": item["Background"], "method": item["Method"], "conclusion": item["Result"]}
        # data_dic["text"] = load_prompt("prompts/segment/build_abstract.md", params)
        data_dic["method"] = item["Method"]
        data_dic["background"] = item["Background"]
        data_dic["conclusion"] = item["Result"]
        data_dics.append(data_dic)
        origin_dics.append({'text': item["Abstract"]})

    save_path = f"Benches/segmentation/final/csvs"
    check_path(save_path)
    save_to_csv(data_dics, save_path, "BrainXBench_SEG_3K")
    save_to_csv(origin_dics, save_path, "BrainXBench_origin_3K")
    print(f"✅: Valid data size is {len(data_dics)}")
    print(f"✅: Successfully saved the data to {save_path}")

def build_True_False_set(path_folder):
    # load all files in the folder
    data = []
    for file in os.listdir(path_folder):
        if file.endswith(".csv"):
            data += load_csv(f"{path_folder}/{file}")
    data_dics = []
    for id, item in enumerate(data):
        print(f"Item.keys: {item.keys()}")
        data_dic = {}
        if item["Intact_or_not"] != 1:
            print(f"❌ Ignore data {id} because it is not intact.")
            continue
        if item["Neuroscience related"] != 1:
            print(f"❌ Ignore data {id} because it is not neuroscience related.")
            continue
        if item["Abstract"] != str(item["Background"]) + ' ' + str(item["Method"]) + ' ' + str(item["Result"]):
            print(f"❌ Ignore data {id} because the abstract is not the combination of Background, Method, and Result.")
            continue
       
        data_dic["method"] = item["Method"]
        data_dic["background"] = item["Background"]
        # randomly shuffle the true and false
        conclusion1 = item["Result"]
        conclusion2 = item["modified conclusion"]
        if random.random() > 0.5:
            data_dic["conclusion1"] = conclusion1
            data_dic["conclusion2"] = conclusion2
            data_dic["label"] = "text 1"
        else:
            data_dic["conclusion1"] = conclusion2
            data_dic["conclusion2"] = conclusion1
            data_dic["label"] = "text 2"


        data_dics.append(data_dic)
        

    save_path = f"Benches/segmentation/final/csvs"
    check_path(save_path)
    save_to_csv(data_dics, save_path, "BrainXBench_TF_3K")
    print(f"✅: Valid data size is {len(data_dics)}")
    print(f"✅: Successfully saved the data to {save_path}")





if __name__ == "__main__":
    if cfg.bench_type == "forward":
        build_brainXbench_forward(bench_name=cfg.bench_name)
        build_brainXbench_forward_multi(bench_name=cfg.bench_name)

