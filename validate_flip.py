import ast
from utils import *
from infos import *
from generate_BrainX import generate_forward
from omegaconf import OmegaConf
# 读取配置
cfg = OmegaConf.load("configs/config.yaml")


if __name__ == "__main__":

    generate_forward(
        task="validate", 
        prompt_path="prompts/forwards/validation.md", 
        source_path=f"workspaces/{cfg.bench_name}/data/forward/flip/flip_data.csv",
        save_path=f"workspaces/{cfg.bench_name}/data/forward/", 
    )

