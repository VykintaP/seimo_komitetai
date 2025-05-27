import requests
import pandas as pd
from pathlib import Path
import time

# Patikriname, ar yra CSV failų 'data/cleaned' aplanke
cleaned_dir = Path("darbotvarkiu_analize/data/cleaned")
print(f"Files found in 'darbotvarkiu_analize/data/cleaned': {list(cleaned_dir.glob('*.csv'))}")

API_URL = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"
HF_TOKEN = "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"  # <- ČIA ĮKLIJUOK SAVO Hugging Face tokeną
headers = {"Authorization": f"Bearer {HF_TOKEN}"}

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

def classify_with_api(question: str) -> str:
    prompt = f"""
Klausimas: "{question}"
Pasirink viena atitinkančią viešosios politikos temą iš šių:
{", ".join(TOPICS)}

Atsakyk tik tema, be jokio paaiškinimo.
"""
    response = requests.post(API_URL, headers=headers, json={"inputs": prompt})

    # Išvedame užklausą ir API atsakymą
    print(f"\nUžklausa:\n{prompt.strip()}")
    print(f"API statusas: {response.status_code}")
    print(f"API atsakymas: {response.text[:500]}...")  # rodome tik pradžią

    if response.status_code != 200:
        print(f"API klaida: Statusas - {response.status_code}, Atsakymas - {response.text}")
        return "API klaida"

    try:
        output = response.json()
        if isinstance(output, list) and "generated_text" in output[0]:
            result = output[0]["generated_text"]
            for topic in reversed(TOPICS):
                if topic in result:
                    return topic
            return "Neatpažinta tema"
        else:
            print("API atsakymas neturi laukiamų duomenų.")
            return "Neteisingas formatas"
    except Exception as e:
        print(f"Klaida apdorojant API atsakymą: {e}")
        return "Neteisingas atsakymas"

def process_files():
    cleaned_dir = Path("darbotvarkiu_analize/data/cleaned")
    classified_dir = Path("darbotvarkiu_analize/data/classified")
    classified_dir.mkdir(parents=True, exist_ok=True)

    # Apdorojame visus CSV failus 'data/cleaned' aplanke
    for file in cleaned_dir.glob("*.csv"):
        output_path = classified_dir / file.name
        print(f"Overwriting {file.name} (reclassifying)")

        print(f"Classifying {file.name} via API...")

        df = pd.read_csv(file)
        if "question" not in df.columns:
            print(f"File {file.name} has no 'question' column, skipping.")
            continue

        df = df.dropna(subset=["question"])
        df["theme"] = df["question"].apply(classify_with_api)

        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")

        # Pridėti vėlavimą tarp užklausų, kad išvengti API apribojimų
        time.sleep(1)

if __name__ == "__main__":
    process_files()
