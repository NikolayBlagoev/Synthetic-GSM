# Synthetic-GSM
Synthetic Dataset Generation for Large Language Model evaluation. The dataset is generated in the style of GSM-8k, thus it contains relatively easy mathematical questions that a bright grade school student should be able to answer. This project is intended for automatic evaluation of LLMs, which have already been trained on similar math questions.

Our approach generates synthetic samples similar to [GSM Symbolic](https://arxiv.org/html/2410.05229v1). We make use of templates where nouns, adjectives, verbs, and numbers are filled randomly to create a coherent question and answer pair. Thus, data should be completely new to the model at evaluation time.

For example, the question-answer pair in the template:
```JSON
"question": "{n1,noun} има формата на правоъгълник с размери {x1,int} м на {x2,int} м. {x3,int,inv-str} е покрита с {n2,noun--cover,n1}, а останалата част - с {n3,noun--cover,n1}. Каква част е покрита с {n3}?",

"answer": "{n1} има площ дължина * широчина ({x1} * {x2} =<<{x1}*x2>>= {area}).\nПлощта на частта покрита с {n2} e {area} / {x3} =<<{area}/{x3}>>= {x4} квадратни метри.\nОстаналата част, покрита с {n3}, е {area} - {x4}=<<{area}-{x4}>>={x5} кв.м.\n### {x5}"
```

Might produce:

```JSON
"question": "Улица има формата на правоъгълник с размери 12 м на 18 м. Една четвърт е покрита с ябълки, а останалата част - с череши. Каква част е покрита с череши?",

"answer": "Улица има площ дължина * широчина (12 * 18 =<<12*x2>>= 216).\nПлощта на частта покрита с ябълки e 216 / 4 =<<216/4>>= 54.0 квадратни метри.\nОстаналата част, покрита с череши, е 216 - 54.0=<<216-54.0>>=162.0 кв.М\n### 162.0"
```


Currently supported languages and number of templates available:
- 🇧🇬 Bulgarian - 18 templates
- 🇬🇧 English - Work In Progress



### Bulgarian

Templates were generated based on questions found in [GSM-8k](https://huggingface.co/datasets/openai/gsm8k), [GSM-8k BG Eval](https://huggingface.co/datasets/INSAIT-Institute/GSM8k-bgeval), and National Exams for fourth grade in [Mathematics](https://www.mon.bg/obshto-obrazovanie/natsionalno-vanshno-otsenyavane-nvo/nvo-za-iv-klas/testove-i-verni-otgovori-ot-nvo-za-iv-klas-po-godini/).


