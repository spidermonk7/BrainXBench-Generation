import os
from utils import *
from infos import *

# "gpt-4o-2024-11-20", 

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
    assert question_type in QS_TYPE, f"Invalid question type: {question_type}. Please choose from {QS_TYPE}"

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
            item["Version"] = BRAIN_X_BENCH_VERSION

        save_to_csv(bench_data, save_path, name=name)
        print(f"✅ Your response of Chapter {i} is saved to {save_path}")
        with open(f"{save_path}/log.txt", "a") as f:
            f.write(f"Processed Chapter {i}\n")


def generate_forward(task, 
                    prompt_path, 
                    source_path, 
                    save_path, 
                    model_name = "gpt-4o", 
                    version = "BrainX-v1", 
                    ):
    """
    Function for generating the forward bench, including two steps: Split and Flip.
    
    (1) Split: Segment the abstract into Background, Method, and Results.
    (2) Flip: Modify Method and Results part, offer incorrect choice for model evaluation. 
    (3) Save the results to a new csv file.

    """

    paper_infos = load_csv(source_path)
    save_path = save_path + task
    check_path(save_path)

    if os.path.exists(save_path + f"/{task}_data.csv"):
        last_id = len(load_csv(save_path + f"/{task}_data.csv"))
    else:
        last_id = -1

    for id, paper_info in enumerate(paper_infos):
        if id < last_id: continue
        if task == "split":
            params = {
                "abstract": paper_info["Abstract"],
            }
        elif task == "flip":
            assert "Background" in paper_info.keys() and "Method" in paper_info.keys() and "Result" in paper_info.keys(), "Background, Method, and Results are required in the csv file."
            params = {
                "background": paper_info["Background"],
                "method": paper_info["Method"],
                "results": paper_info["Result"],
            }
        elif task == "validate":
            params = {
            "initial_conclusion": paper_info["Result"],
            "Opposite_Outcome": paper_info["Opposite_Outcome"],
            "Factor_Misattribution": paper_info["Factor_Misattribution"],
            "Incorrect_Causal_Relationship": paper_info["Incorrect_Causal_Relationship"],
            }
        prompt = load_prompt(prompt_path, params)
        with timer("Benchmarks Generation"):
            print(f"🤖: Your {model_name} question generator is processing abstract {id}")
            try:
                output = LLM_response(prompt=prompt, model_name=model_name)
                response = eval(output.strip())
                print(f"Successfully evaluate the response to type {type(response)}")
            except:
                print(f"❌: Error occurs when processing abstract {id}.")
                print(f"❌: Response: {output}")
                with open(f"{save_path}/error.log", "a") as f:
                    f.write(f"Error occurs when processing abstract {id}, program exits.\n")
                    f.write(f"Response: {output}")
                raise ValueError(f"Error occurs when processing abstract {id} for bench: {version}.")
        
        for key in response.keys():
            paper_info[key] = response[key]
       
        bench_data = [paper_info]
        save_to_csv(bench_data, save_path, f"{task}_data")
        print(f"✅ Process results of abstract {id} is saved to {save_path}")


