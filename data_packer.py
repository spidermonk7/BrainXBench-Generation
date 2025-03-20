import pandas as pd
from utils import *
from infos import *
from argparse import ArgumentParser

def pack_data(data_path):
    csv_data = load_csv(data_path)
    df = pd.DataFrame(csv_data)
    path = data_path[:data_path.rfind("/")]
    check_path(path.replace("csv", "parquet"))
    check_path(path.replace("csv", "json"))
    df.to_parquet(data_path.replace("csv", "parquet"), index=False)
    df.to_json(data_path.replace("csv", "json"), orient="records")

    print(f"✅: Successfully saved the data to {data_path.replace('csv', 'parquet')} and {data_path.replace('csv', 'json')}")
 

if __name__ == "__main__":
    args = ArgumentParser()
    args.add_argument("-V", type = float, default = 0.6, help = "The bench version corresponding to your own prompt")

    args = args.parse_args()
    pathes = [
        f"Benches/forward/final/csvs/Incorrect_Causal_Relationship-V{args.V}.csv", 
        f"Benches/forward/final/csvs/Opposite_Outcome-V{args.V}.csv",
        f"Benches/forward/final/csvs/Factor_Misattribution-V{args.V}.csv"
    ]
    # for path in pathes:
    #     pack_data(path)

    # # python data_packer.py -V your_bench_version

    # pathes = [
    #     "Benches/backward/final/csvs/BrainXBench_CHOICE.csv",
    #     "Benches/backward/final/csvs/BrainXBench_CHOICE_mini.csv"
    # ]
    # for path in pathes:
    #     pack_data(path)


    pathes = [
        "Benches/backward/csvs/BrainXBench_TEXT_full.csv"
    ]
    for path in pathes:
        pack_data(path)