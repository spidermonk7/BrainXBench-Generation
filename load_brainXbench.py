import sys
import os

# 获取当前脚本的上级目录（即 `BrainX-NeuroBench`）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .utils import load_csv
from .infos import *



def load_brainXbench_forward(result_type, path ="Benches/forward/flip/v_direct4.0.csv"):
    """
    Function for loading brainXbench forward data
    Required:
    (1) The path of the csv file
    (2) Combination of the data: Background, Method, Conclusion

    Return:
    (1) List of dictionary with fake_abstract and true_abstract
    """
    bench_data = load_csv(path)
    bench_dics = []
    for item in bench_data:
        bench_dic = {}
       
        fake_abstract = item["Background"] + ' ' + item["Method"] + ' ' + item[result_type]

        bench_dic["true_abstract"] = item["Abstract"]
        bench_dic["fake_abstract"] = fake_abstract
        

        bench_dics.append(bench_dic)

    return bench_dics
        

def load_brainXbench_backward(question_type, mini):
    if mini:
        path = f"Benches/backward/BrainXBench_{question_type}_mini.csv"
    else:
        if question_type == "TF":
            raise ValueError("❌: The full version of TF is not available.")
        path = f"Benches/backward/BrainXBench_{question_type}.csv"
    bench_data = load_csv(path)

    return bench_data
    
