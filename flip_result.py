from utils import *
from infos import *
from generate_BrainX import generate_forward
from argparse import ArgumentParser
from omegaconf import OmegaConf

# 读取配置
cfg = OmegaConf.load("configs/config.yaml")

if __name__ == "__main__":
    generate_forward('flip', 
                    prompt_path='prompts/forwards/flip.md',
                    source_path=f'workspaces/{cfg.bench_name}/data/forward/split/split_valids.csv',
                    save_path=f'workspaces/{cfg.bench_name}/data/forward/',
                    version=cfg.bench_name,
                    )