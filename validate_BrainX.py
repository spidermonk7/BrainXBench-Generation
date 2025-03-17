import sys
import os

# 获取当前脚本的上级目录（即 `BrainX-NeuroBench`）
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils import *
from infos import *
from argparse import ArgumentParser



def validate_bench(task, 
                    prompt_path, 
                    source_path, 
                    save_path, 
                    model_name = "gpt-4o"
                    ):
    """
    Function for generating the forward bench, including two steps: Split and Flip.
    
    (1) Split: Segment the abstract into Background, Method, and Results.
    (2) Flip: Modify Method and Results part, offer incorrect choice for model evaluation. 
    (3) Save the results to a new csv file.

    """

    # TODO:
    # (1) The saving logic should be redirected to a new path. 

    brainXBench = load_csv(source_path)
    save_path = save_path + task + '/csvs'
    check_path(save_path)
    for id, paper_info in enumerate(brainXBench):
        if id < 73: continue
        params = {
            "initial_conclusion": paper_info["Result"],
            "Opposite_Outcome": paper_info["Opposite_Outcome"],
            "Factor_Misattribution": paper_info["Factor_Misattribution"],
            "Incorrect_Causal_Relationship": paper_info["Incorrect_Causal_Relationship"],
        }
        
        prompt = load_prompt(prompt_path, params)
        # print(f"prompts are loaded: {prompt}")
        with timer("Benchmarks Validation"):
            print(f"🤖: Your {model_name} question checker is validating modifications {id} from journal {paper_info['Source']}, DOI: {paper_info['DOI']}")
            response = LLM_response(prompt=prompt, model_name=model_name)

        try:
            print(f"type of response: {type(response)}")
            # response = parse_json_response(response)
            response = eval(response)
            print(f"Successfully evaluate the response to type {type(response)}")
        except:
            print(f"❌: Error occurs when processing abstract {id}.")
            print(f"❌: Response: {response}")
            continue
        
        for key in response.keys():
            paper_info[key] = response[key]
       
        bench_data = [paper_info]

        save_to_csv(bench_data, save_path, "valids_v_direct0.6")
        print(f"✅ Process results of abstract {id} is saved to {save_path}")




if __name__ == "__main__":
    validate_bench(
        task="flip", 
        prompt_path="prompts/forwards/validation.md",
        source_path="Benches/forward/flip/csvs/v_direct0.6.csv",
        save_path="Benches/forward/", 
    )