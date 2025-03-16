import pandas as pd
from utils import *
from infos import *


def pad_data(path):
    csv_data = load_csv(path)
    df = pd.DataFrame(csv_data)
    # save it to parquet
    df.to_parquet(path.replace(".csv", ".parquet"), index=False)
    print(f"✅: Successfully saved the data to {path.replace('.csv', '.parquet')}")

    # save it to json
    df.to_json(path.replace(".csv", ".json"), orient="records")


if __name__ == "__main__":
    path = "Benches/forward/flip/v_direct0.4.csv"
    pad_data(path)