from utils import *
from omegaconf import OmegaConf
from tqdm import tqdm
# 读取配置
cfg = OmegaConf.load("configs/back_config.yaml")


def generate_backward(question_type, 
                    prompt_path, 
                    source_path, 
                    save_path, 
                    model_name = "gpt-4o", 
                    question_num = 10, 
                    book_name = "Koch", 
                    name = "v1", 
                    ):
    """
    Function for generating the backward bench, Supporting three question types. 
    (1) CHOICE: Choose a correct discription from the given two options.
    (2) TRUE_FALSE: Judge true or false for a description. 
    (3) QA: Answer a question. 
    """
    assert question_type in cfg.QS_TYPE, f"Invalid question type: {question_type}. Please choose from {cfg.QS_TYPE}"

    # get last id in log file
    if os.path.exists(f"{save_path}/log.txt"):
        with open(f"{save_path}/log.txt", "r") as f:
            lines = f.readlines()
            last_id = len(lines)
        print(f"📚: Proceesed {last_id} chapters in {save_path}")
    else:
        last_id = -1

    txt_files = load_txt_files(source_path)
    print(f"📚: Found {len(txt_files)} chapters in {source_path}")
    for i, txt in enumerate(txt_files):
        if i < last_id: continue
        params = {
            "source_txt": txt,
            "question_num": question_num
        }
        prompt = load_prompt(prompt_path, params)

        with timer("Benchmarks Generation"):
            print(f"🤖: Your {model_name} model is generating benchmark {i}, please wait...")
            response = LLM_response(prompt=prompt, model_name=model_name)
        print(f"type of response: {type(response)}")
        response = eval(response)
        bench_data = [backward_data for _, backward_data in response.items()]

        # add a key "Chapter" to each item
        for item in bench_data:
            item["Chapter"] = i + 1
            item["Book"] = book_name
            item["Version"] = name

        save_to_csv(bench_data, save_path, name=name)
        with open(f"{save_path}/log.txt", "a") as f:
            f.write(f"Processed Chapter {i}\n")


def split_and_convert_pdf(input_pdf, output_folder, page_ranges):
    """
    按指定页码范围拆分 PDF，并将拆分后的 PDF 转换为 TXT。
    
    :param input_pdf: 输入 PDF 文件路径
    :param output_folder: 存储拆分后 PDF 和 TXT 文件的文件夹
    :param page_ranges: 页码范围列表，如 [(2,5), (7,19)] 表示 2-5 页为一个文件，7-19 页为另一个文件
    """
    # 确保输出文件夹存在
    os.makedirs(output_folder, exist_ok=True)
    if type(page_ranges) == int:
        page_ranges = [(i, i + page_ranges) for i in range(49, 1581, page_ranges + 1)]
    

    # 打开 PDF
    doc = fitz.open(input_pdf)

    for idx, (start_page, end_page) in tqdm(enumerate(page_ranges), desc="📚: Processing PDF", total=len(page_ranges)):
        # 处理页码（PyMuPDF 的页码从 0 开始，因此要减 1）
        start_page -= 1
        end_page -= 1

        # 创建新 PDF 文档
        new_pdf = fitz.open()
        new_pdf.insert_pdf(doc, from_page=start_page, to_page=end_page)

        # 生成文件名（PDF & TXT）
        pdf_filename = os.path.join(output_folder, f"Chapter_{idx+1}[{start_page+1}-{end_page+1}].pdf")
        txt_filename = os.path.join(output_folder, f"Chapter_{idx+1}_[{start_page+1}-{end_page+1}].txt")

        # 保存拆分的 PDF
        new_pdf.save(pdf_filename)
        new_pdf.close()

        # 转换 PDF 为 TXT
        convert_pdf_to_text(pdf_filename, txt_filename)

    doc.close()
    print("✅ 所有 PDF 拆分 & 转换 TXT 任务完成！")


def convert_pdf_to_text(input_pdf, output_txt):
    """
    将 PDF 解析为 TXT 文件
    :param input_pdf: PDF 文件路径
    :param output_txt: 输出 TXT 文件路径
    """
    doc = fitz.open(input_pdf)
    with open(output_txt, "w", encoding="utf-8") as f:
        for page_num in range(len(doc)):
            text = doc[page_num].get_text("text")  # 提取纯文本
            f.write(f"===== Page {page_num + 1} =====\n")
            f.write(text + "\n\n")
    


if __name__ == "__main__":
    book_name = cfg.bookname
    input_pdf = cfg.BOOK_INFO_DICT[book_name]["PDF"]
    output_folder = cfg.BOOK_INFO_DICT[book_name]["source_path"] + "/chapters/"

    # split_and_convert_pdf(input_pdf=input_pdf, output_folder=output_folder, page_ranges=cfg.pages_per_chapter)

    prompt_path = f"prompts/backwards/{cfg.task_type}_QA.md"
    source_path = cfg.BOOK_INFO_DICT[cfg.bookname]["source_path"] + "/chapters/"
    save_path = f"workspaces/{cfg.bench_name}/bench/backward/"
    check_path(save_path)
    generate_backward(
        cfg.task_type, prompt_path, source_path, 
        save_path = save_path, book_name=cfg.bookname, 
        question_num = cfg.BackQS_num, 
        name = f"BrainXBench_{cfg.task_type}"
        )
