from generate_BrainX import generate_backward
from utils import *
from omegaconf import OmegaConf
# 读取配置
cfg = OmegaConf.load("configs/config.yaml")





if __name__ == "__main__":
    book_name = cfg.bookname
    input_pdf = cfg.BOOK_INFO_DICT[book_name]["PDF"]
    output_folder = cfg.BOOK_INFO_DICT[book_name]["source_path"] + "/chapters/"

    split_and_convert_pdf(input_pdf=input_pdf, output_folder=output_folder, page_ranges=cfg.pages_per_chapter)

    prompt_path = f"prompts/backwards/{cfg.task_type}_QA.md"
    source_path = cfg.BOOK_INFO_DICT[cfg.bookname]["source_path"] + "/chapters/"
    save_path = f"workspaces/{cfg.bench_name}/data/backward/"
    check_path(save_path)
    generate_backward(
        cfg.task_type, prompt_path, source_path, 
        save_path = save_path, book_name=cfg.bookname, 
        question_num = cfg.BackQS_num, 
        name = f"BrainXBench_{cfg.task_type}"
        )
