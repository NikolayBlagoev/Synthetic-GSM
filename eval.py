import transformers
import torch
import random
random.seed(42)
from itertools import combinations
from transformers import GenerationConfig
import gc
from math import isclose
from run import run
from string import punctuation
from transformers import AutoTokenizer, AutoModelForCausalLM
generation_params = GenerationConfig(
    max_new_tokens=1024,              
    do_sample = False,
    top_k=1,
    top_p=1,
    repetition_penalty=1.1,
    eos_token_id=[1]
)
token = ""
model_id = "INSAIT-Institute/BgGPT-Gemma-2-9B-IT-v1.0"
model_id = "meta-llama/Meta-Llama-3.1-8B-Instruct"
model_id = "google/gemma-2-9b-it"
tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    use_default_system_prompt=False,
    token = token
)
model = AutoModelForCausalLM.from_pretrained(model_id,
    torch_dtype=torch.bfloat16,
    attn_implementation="eager",
    device_map="cuda")


def generate_prompt_bg(ds,shots = 8):
    txt = ""
    # print(len(ds))
    order = random.sample(list(range(len(ds["question"]))),shots+1)
    txt += "Реши следните математически задачи стъпка по стъпка:\n"
    
    for el in order[:-1]:
        
        
        txt += f"Q: {ds["question"][el]}"
        txt += f"\nA: Нека решим задачата стъпка по стъпка. {ds["answer"][el]}. Тъй че отговорът е {ds["num_answer"][el]}\n"
    
    txt += f"Q: {ds["question"][order[-1]]}"
    txt += f"\nA: "
    return txt, ds["num_answer"][order[-1]], ds["answer"][order[-1]], ds["question"][order[-1]]




correct = 0
generate_ds = run(12,[1,50])
print(len(generate_ds["question"]))
inaccuracy = []
for _ in range(100):
    print("-------------------------------------")
    print(correct)
    prompt, final_num, final_a, final_q = generate_prompt_bg(generate_ds)
    messages = [
        {"role": "user", "content": prompt},
    ]
    input_ids = tokenizer(
        prompt,
        return_tensors="pt"
    ).to("cuda")

    outputs = model.generate(
        **input_ids,
        generation_config=generation_params
    )
    ans = tokenizer.decode(outputs[0])
    #print(prompt)
    # print(ans)
    # print(final_num)
    ans = ans.split(" ")
    i = len(ans)
    
    ret = None
    while i > 0:
        i -= 1
        try:
            while len(ans[i]) > 0:
                if ans[i][-1] in "!.,':;-+?*":
                    ans[i] = ans[i][:-1]
                elif ans[i][0] in "!.,':;-+?*":
                    ans[i] = ans[i][1:]
                else:
                    break
            if len(ans[i]) < 1:
                continue
            ret = float(ans[i].strip(punctuation).strip())
            break
        except ValueError:
            continue
    if ret != None and isclose(final_num,ret,abs_tol=0.01):
        with open("f1.txt","a",encoding="utf-8") as fd:
            fd.writelines("-------------\n")
            fd.writelines("CORRECT ANSWER!!\n")
            fd.writelines(final_q + "\n")
            fd.writelines(final_a + "\n")
            fd.writelines(str(ret) + "\n" )
            fd.writelines(" ".join(ans))
        correct += 1
    else:
        with open("f1.txt","a",encoding="utf-8") as fd:
            fd.writelines("-------------\n")
            fd.writelines("INCORRECT ANSWER!!\n")
            fd.writelines(final_q + "\n")
            fd.writelines(final_a + "\n")
            fd.writelines(str(ret) + "\n")
            fd.writelines(" ".join(ans))
        inaccuracy.append(abs(final_num-ret)/(1e-6+ret))
            
print(correct/100)
print(sum(inaccuracy)/len(inaccuracy))