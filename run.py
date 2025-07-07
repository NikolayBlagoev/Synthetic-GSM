from interpreter import process_string, post_process
import re
from k_base import load_knowledge_base
from sys import argv
import json
from itertools import product
from mathematical_interpreter import *
from linguistic_interpreter import *
kb = load_knowledge_base()



def run(question_count,rng):
    df = {'question': [], 'answer': [], 'type': [], 'num_answer': []}
    duplicate_check = {}
    if len(rng) == 1:
        rng = [rng]
    elif len(rng) == 2:
        rng = list(range(rng[0],rng[1]))
    for _ in range(question_count):
        for i in rng:
            print(i)
            with open(f"templates/q{i}.json","r",encoding="utf-8") as fp:
                tmp = json.load(fp)
                word_solutions = get_all_words(tmp["question"],tmp["answer"],tmp["word-conditions"],kb)
                numerical_solutions = get_all_numbers(tmp["question"],tmp["answer"],tmp["conditions"])
                
                if len(word_solutions) == 0:
                    word_solutions.append({})
                
                # exit()
                # print(numerical_solutions)
                for ns,ws in product(numerical_solutions,word_solutions):
                    
                        code_results = {}
                        for k,code in tmp["code-execution"].items():
                            while True:
                                r = re.search('`(.*?)`', code)
                                if r == None:
                                    break
                                item = r.group(1)
                                code = code[:r.span()[0]] + f"ns['{item}']" + code[r.span()[1]:]
                                
                            code_results[k] = str(eval(code))
                            
                        prev_state = {}
                        prev_noun = ""
                    
                        question,prev_state,prev_noun = process_string(tmp["question"],ws,ns,prev_state,prev_noun,code_results,kb)
                        question = post_process(question)
                        if question in duplicate_check:
                            continue
                        duplicate_check[question] = True
                        answer, _, _ = process_string(tmp["answer"],ws,ns,prev_state,prev_noun,code_results,kb)
                        answer = post_process(answer)
                        num_answer,_,_ = process_string(tmp["num-answer"],ws,ns,prev_state,prev_noun,code_results,kb)
                        num_answer = float(num_answer)
                        # print(i, "Q:", question,"\n A: ",answer)
                        df["question"].append(question)
                        df["answer"].append(answer)
                        df["type"].append(tmp["type"])
                        df["num_answer"].append(num_answer)
                        # print("--------------")
                        break
    return df
if __name__ == "__main__":
    rng = argv[1]
    if "-" in rng:
        rng = rng.split("-")
        rng[0] = int(rng[0].strip())
        rng[1] = int(rng[1].strip())
    else:
        rng = [rng,0]
        rng[0] = int(rng[0].strip())
        rng[1] = rng[0]  + 1
    question_count = int(argv[2])

    import pandas as pd
    df = run(question_count,rng)
    df = pd.DataFrame(data=df)
    df.to_csv("results/test.csv", index=False)
                
            