import os
os.environ["TRANSFORMERS_CACHE"] = "E:/hf_models_cache"

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline


import torch

model_id = "mistralai/Mistral-7B-Instruct-v0.1"

tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="E:/hf_cache")
model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float16, device_map="auto", cache_dir="E:/hf_cache")
classifier = pipeline("text-generation", model=model, tokenizer=tokenizer)

TOPICS = [
    "Valstybės valdymas, regioninė politika ir viešasis administravimas",
    "Aplinka, miškai ir klimato kaita",
    "Energetika",
    "Viešieji finansai",
    "Ekonomikos konkurencingumas ir valstybės informaciniai ištekliai",
    "Valstybės saugumas ir gynyba",
    "Viešasis saugumas",
    "Kultūra",
    "Socialinė apsauga ir užimtumas",
    "Transportas ir ryšiai",
    "Sveikata",
    "Švietimas, mokslas ir sportas",
    "Teisingumas",
    "Užsienio politika",
    "Žemės ir maisto ūkis, kaimo plėtra ir žuvininkystė"
]


def classify_with_mistral(question: str, max_tokens: int = 50) -> str:
    prompt = f"""
Klausimas: "{question}"
Pasirink viena atitinkančia viešosios politikos temą iš šių:
{", ".join(TOPICS)}

Atsakyk tik tema, be jokio paaiškinimo.
"""
    result = classifier(prompt, max_new_tokens=max_tokens, do_sample=False)[0]["generated_text"]

    for topic in reversed(TOPICS):
        if topic in result:
            return topic
    return "Nežinoma"
