import ast
from utils import *
from infos import *
from argparse import ArgumentParser
from generate_BrainX import generate_forward


if __name__ == "__main__":

    args = ArgumentParser()
    args.add_argument('-B', "--bench_name", type=str, default="BrainX-v1")
    args = args.parse_args()


    generate_forward(
        task="validate", 
        prompt_path="prompts/forwards/validation.md", 
        source_path=f"workspaces/{args.bench_name}/data/forward/flip/flip_data.csv",
        save_path=f"workspaces/{args.bench_name}/data/forward/", 
    )


    # python validate_BrainX.py -V your_bench_version -pv your_prompt_for_validation.md