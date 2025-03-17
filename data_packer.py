import pandas as pd
from utils import *
from infos import *


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
    path = "Benches/forward/flip/csvs/v_direct0.4.csv"
    path = "Benches/backward/csvs/BrainXBench_TEXT.csv"
    path = "Benches/backward/csvs/BrainXBench_TEXT_mini.csv"
    path = "Benches/forward/final/csvs/Incorrect_Causal_Relationship-V0.6.csv"
    # path = "Benches/forward/final/csvs/Opposite_Outcome-V0.6.csv"
    pack_data(path)