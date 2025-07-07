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
    eos_token_id=[1,107]
)
token = ""
model_id = "INSAIT-Institute/BgGPT-Gemma-2-9B-IT-v1.0"

tokenizer = AutoTokenizer.from_pretrained(
    model_id,
    use_default_system_prompt=False,
    token = token
)
model = AutoModelForCausalLM.from_pretrained(model_id,
    torch_dtype=torch.bfloat16,
    attn_implementation="eager",
    device_map="cuda")


def generate_prompt_bg(q_id, shots = 8):
    rnd_sample = random.sample([i for i in range(1,51) if i != q_id], shots * 2)
    generate_ds = run(1,rnd_sample)
    txt = ""
    # print(len(ds))
    # order = random.sample(list(range(len(ds["question"]))),shots+1)
    txt += "Реши следните математически задачи стъпка по стъпка:\n"
    # print(generate_ds)
    for el in range(len(generate_ds["question"])):
        if el > 8:
            break
        
        
        txt += f"Q:" + generate_ds["question"][el]
        txt += f"\nA: Нека решим задачата стъпка по стъпка. " + generate_ds["answer"][el] + ". Тъй че отговорът е " + generate_ds["num_answer"][el] + "\n"
    generate_ds = run(1,[q_id,q_id+1])
    txt += f"Q: " + generate_ds["question"][0]
    txt += f"\nA: "
    return txt, generate_ds["num_answer"][0], generate_ds["answer"][0], generate_ds["question"][0]






inaccuracy = []
for q_id in range(1,51):
    correct = 0
    for _ in range(10):
        print("-------------------------------------")
        
        prompt, final_num, final_a, final_q = generate_prompt_bg(q_id)
        
        messages = [
            {"role": "user", "content": prompt},
        ]
        input_ids = tokenizer(
            prompt,
            return_tensors="pt"
        ).to("cuda")

        outputs = model.generate(
            **input_ids,
            use_cache = False,
            generation_config=generation_params
        )
        ans = tokenizer.decode(outputs[0])
        
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
                
    print(q_id,correct/10)
    if len(inaccuracy) > 0:
        print(q_id,sum(inaccuracy)/len(inaccuracy))