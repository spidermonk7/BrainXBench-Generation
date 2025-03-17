from utils import *
from infos import *



def load_brainXbench_forward(result_type, path ="Benches/forward/flip/csvs/v_direct0.6.csv"):
    """
    Function for loading brainXbench forward data
    Required:
    (1) The path of the csv file
    (2) Combination of the data: Background, Method, Conclusion

    Return:
    (1) List of dictionary with fake_abstract and true_abstract
    """
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
            bench_dic["true_abstract"] = item["Abstract"]
            bench_dic["fake_abstract"] = fake_abstract
           
            if item[f"valid: {result_type}"] == 1:
                bench_dics.append(bench_dic)
        save_path = f"Benches/forward/final/csvs"
        check_path(save_path)
        save_to_csv(bench_dics, save_path, f"{result_type}-V0.6")
        print(f"✅: Successfully saved the data to {save_path}")




if __name__ == "__main__":
    path = "Benches/forward/flip/csvs/valids_v_direct0.6.csv"
    build_brainXbench_forward(path)