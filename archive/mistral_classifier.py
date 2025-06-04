import os
os.environ["TRANSFORMERS_CACHE"] = "E:/hf_models_cache"

from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline
import torch

# "truksta"
)


tokenizer = AutoTokenizer.from_pretrained(model_id, cache_dir="E:/hf_cache")
model = AutoModelForCausalLM.from_pretrained(
    model_id,
    torch_dtype=torch.float32,
    device_map="auto",
    cache_dir="E:/hf_cache"
)
classifier = pipeline("text-generation", model=model, tokenizer=tokenizer)
assifier = pipeline("text-generation", model=model, tokenizer=tokenizer)

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

if __name__ == "__main__":
    import pandas as pd
    from pathlib import Path

    cleaned_dir = Path("data/cleaned")
    classified_dir = Path("data/classified")
    classified_dir.mkdir(parents=True, exist_ok=True)

    for file in cleaned_dir.glob("*.csv"):
        output_path = classified_dir / file.name
        if output_path.exists():
            print(f"Skipping {file.name} (already classified)")
            continue

        print(f"Classifying {file.name}...")

        df = pd.read_csv(file)
        if "question" not in df.columns:
            print(f"File {file.name} has no 'question' column, skipping.")
            continue

        df = df.dropna(subset=["question"])
        df["theme"] = df["question"].apply(classify_with_mistral)

        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")
