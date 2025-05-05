from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
from math import isclose
tokenizer = AutoTokenizer.from_pretrained(
    "INSAIT-Institute/BgGPT-Gemma-2-9B-IT-v1.0",
    use_default_system_prompt=False,
)

def draw_question():
    return {"q": "Аз съм ники", "a": "Ти не си ники", "f": 45}
def generate_prompt_bg(shots = 8):
    txt = ""

    txt += "Реши следните математически задачи стъпка по стъпка:\n"
    for el in range(shots):
        q = draw_question()
        txt += f"Q: {q["q"]}"
        txt += f"A: Нека решим задачата стъпка по стъпка. {q["a"]}. Тъй че отговорът е {q["f"]}\n"
    final_q = draw_question()
    txt += f"Q: {final_q["q"]}"
    txt += f"A: "
    return txt, final_q



model = AutoModelForCausalLM.from_pretrained(
    "INSAIT-Institute/BgGPT-Gemma-2-9B-IT-v1.0",
    torch_dtype=torch.bfloat16,
    attn_implementation="eager",
    device_map="auto",
)



correct = 0
for _ in range(1000):
    
    prompt, final_q = generate_prompt_bg()
    messages = [
        {"role": "user", "content": prompt},
    ]
    input_ids = tokenizer.apply_chat_template(
        messages,
        return_tensors="pt",
        add_generation_prompt=True,
        return_dict=True
    )

    outputs = model.generate(
        **input_ids,
        generation_config=generation_params
    )
    ans = tokenizer.decode(outputs[0])
    ans = ans.split(" ")
    i = len(ans)
    ret = None
    while i > 0:
        i -= 1
        try:
            ret = float(ans[i].strip())
        except ValueError:
            continue
    if ret != None and isclose(final_q["f"],ret):
        correct += 1
            
print(correct/1000)