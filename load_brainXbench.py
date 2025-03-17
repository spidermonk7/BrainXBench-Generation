from utils import *
from infos import *
import random



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
    



# Opposite_Outcome	Incorrect_Causal_Relationship	Factor_Misattribution	Balderdash	modification: Opposite_Outcome	valid: Opposite_Outcome	modification: Factor_Misattribution	valid: Factor_Misattribution	modification: Incorrect_Causal_Relationship	valid: Incorrect_Causal_Relationship

def build_brainXbench_forward(raw_path):
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

        save_path = f"Benches/forward/final/csvs"
        check_path(save_path)
        # check if the file exist
        if os.path.exists(f"{save_path}/{result_type}-V0.6.csv"):
            print(f"💁: The file {result_type}-V0.6.csv already exists.")
            os.remove(f"{save_path}/{result_type}-V0.6.csv")
            save_to_csv(bench_dics, save_path, f"{result_type}-V0.6")
        else:
            save_to_csv(bench_dics, save_path, f"{result_type}-V0.6")
            print(f"✅: Successfully saved the data to {save_path}")






if __name__ == "__main__":
    path = "Benches/forward/flip/csvs/valids_v_direct0.6.csv"
    build_brainXbench_forward(path)

    load_brainXbench_forward("Opposite_Outcome")
    load_brainXbench_forward("Incorrect_Causal_Relationship")
    load_brainXbench_forward("Factor_Misattribution")