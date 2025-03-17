import sys
import os

# 获取当前脚本的上级目录（即 `BrainX-NeuroBench`）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *
from infos import *
from argparse import ArgumentParser

# "gpt-4o-2024-11-20", 

def generate_backward(question_type, 
                    prompt_path, 
                    source_path, 
                    save_path, 
                    model_name = "gpt-4o", 
                    question_num = 10, 
                    book_name = "Koch", 
                    name = "v1"
                    ):
    """
    Function for generating the backward bench, Supporting three question types. 
    (1) CHOICE: Choose a correct discription from the given two options.
    (2) TRUE_FALSE: Judge true or false for a description. 
    (3) QA: Answer a question. 
    """
    assert question_type in QS_TYPE, f"Invalid question type: {question_type}. Please choose from {QS_TYPE}"

    txt_files = load_txt_files(source_path)
    print(f"📚: Found {len(txt_files)} chapters in {source_path}")
    for i, txt in enumerate(txt_files):
        if i < 186: continue
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
            item["Version"] = BRAIN_X_BENCH_VERSION

        save_to_csv(bench_data, save_path, name=name)
        print(f"✅ Your response of Chapter {i} is saved to {save_path}")



def generate_forward(task, 
                    prompt_path, 
                    source_path, 
                    save_path, 
                    model_name = "gpt-4o", 
                    version = 0.6
                    ):
    """
    Function for generating the forward bench, including two steps: Split and Flip.
    
    (1) Split: Segment the abstract into Background, Method, and Results.
    (2) Flip: Modify Method and Results part, offer incorrect choice for model evaluation. 
    (3) Save the results to a new csv file.

    """

    # TODO:
    # (1) The saving logic should be redirected to a new path. 

    paper_infos = load_csv(source_path)
    save_path = save_path + task + '/csvs'
    check_path(save_path)
    for id, paper_info in enumerate(paper_infos):

        if task == "split":
            params = {
                "abstract": paper_info["Abstract"],
            }
         

        elif task == "flip":
            # print(paper_info.keys())
            assert "Background" in paper_info.keys() and "Method" in paper_info.keys() and "Result" in paper_info.keys(), "Background, Method, and Results are required in the csv file."
            params = {
                "background": paper_info["Background"],
                "method": paper_info["Method"],
                "results": paper_info["Result"],
            }
        
        prompt = load_prompt(prompt_path, params)
        with timer("Benchmarks Generation"):
            print(f"🤖: Your {model_name} question generator is processing abstract {id} from journal {paper_info['Source']}, DOI: {paper_info['DOI']}")
            response = LLM_response(prompt=prompt, model_name=model_name)

        try:
            print(f"type of response: {type(response)}")
            response = eval(response)
            print(f"Successfully evaluate the response to type {type(response)}")
        except:
            print(f"❌: Error occurs when processing abstract {id}.")
            print(f"❌: Response: {response}")
            continue
        
        for key in response.keys():
            paper_info[key] = response[key]
       
        bench_data = [paper_info]

        save_to_csv(bench_data, save_path, f"v_direct{version}")
        print(f"✅ Process results of abstract {id} is saved to {save_path}")



if __name__ == "__main__":
    args = ArgumentParser()

    args.add_argument("--task_type", type = str, default = "CHOICE", help = "Choose from CHOICE, TRUE_FALSE, QA for Backward and Flip or Split for Forward.")
    args.add_argument("--bookname", type = str, default = "Koch", help = "The book name for the backward bench.")
    args.add_argument("--bench_type", type = str, default = "forwards", help = "The bench type for the backward bench.")
    args.add_argument("--BackQS_num", type = int, default = 10, help = "The number of questions for each chapter.")
    args.add_argument("-V", type = float, default = 0.6, help = "The bench version corresponding to your own prompt")
    args = args.parse_args()


    if args.bench_type == "backward":
        question_type = args.task_type
        prompt_path = f"prompts/backwards/{question_type}_QA.md"
        source_path = BOOK_INFO_DICT[args.bookname]["source_path"] + "/chapters/"
        save_path = f"Benches/{args.bench_type}"
        check_path(save_path)
        # save_path += f"BrainXBench_{question_type}_v2"
        generate_backward(
            question_type, prompt_path, source_path, 
            save_path = save_path, book_name=args.bookname, 
            question_num = args.BackQS_num, 
            name = f"BrainXBench_{question_type}_v{args.V}"
            )

    elif args.bench_type == "forwards":
        # path = "data/neuroscience/pubmed/v1.csv"
        save_path = f"Benches/forward/"
        check_path(save_path)

        # # Check if the raw data(raw abstracts) are valid, this would save the valid data to valids.csv
        # path = "data/pubmed/data.csv"
        # check_abs(path, "data/pubmed")

        # Analyse the raw abstract data, filter out the top-10 journals with good fame and high quality.
        # This would save the filtered data to data/pubmed/filtered_journals.csv
        path = "data/pubmed/valids.csv"
        raw_abs_ana(path)

        # Generate the forward bench, including two steps: Split and Flip.
        # This would save the results to split/v1.csv and flip/v1.csv
        path = "data/pubmed/selected_data.csv"
    
        # generate_forward("split", "prompts/forwards/split.md", path, save_path)

        # # Check the validation of the split data
        # # This would save the valid data to split/v1_valids.csv
        # check_split_result("Benches/forward/split/v_direct2.0.csv", save=True)
        # check_validation("Benches/forward/split/splited_valids.csv", save_path="Benches/forward/split")  

        # Generate the flip bench
        # This would save the data to flip/v1.csv
        valid_split_path = "Benches/forward/split/v2_valids_sum.csv"
        model_name = 'gpt-4o'
        generate_forward("flip", f"prompts/forwards/flip-v{args.V}.md", valid_split_path, save_path, model_name=model_name)


  
    else:
        raise ValueError("Invalid bench type, please choose from backwards and forwards.")
    

# python generate_BrainX.py --task_type CHOICE --bookname Koch --bench_type backward --BackQS_num 10
# python generate_BrainX.py --bench_type forwards