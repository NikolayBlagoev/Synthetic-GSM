# Synthetic-GSM
Synthetic Dataset Generation for Large Language Model evaluation. The dataset is generated in the style of GSM-8k, thus it contains relatively easy mathematical questions that a bright grade school student should be able to answer. This project is intended for automatic evaluation of LLMs, which have already been trained on similar math questions.

Our approach generates synthetic samples similar to [GSM Symbolic](https://arxiv.org/html/2410.05229v1). We make use of templates where nouns, adjectives, verbs, and numbers are filled randomly to create a coherent question and answer pair. Thus, data should be completely new to the model at evaluation time.


Currently supported languages and number of templates available:
- 🇧🇬 Bulgarian - 18 templates
- 🇬🇧 English - Work In Progress



### Bulgarian

Templates were generated based on questions found in [GSM-8k](https://huggingface.co/datasets/openai/gsm8k), [GSM-8k BG Eval](https://huggingface.co/datasets/INSAIT-Institute/GSM8k-bgeval), and National Exams for fourth grade in [Mathematics](https://www.mon.bg/obshto-obrazovanie/natsionalno-vanshno-otsenyavane-nvo/nvo-za-iv-klas/testove-i-verni-otgovori-ot-nvo-za-iv-klas-po-godini/).


