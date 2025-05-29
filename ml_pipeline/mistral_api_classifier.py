import requests
import pandas as pd
from pathlib import Path
import time
from deep_translator import GoogleTranslator

HF_TOKEN = "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"

# mistral-7b-instruct-v0-1-hdx
API_URL = "https://knja4utso3nn54pk.us-east4.gcp.endpoints.huggingface.cloud"

# autentifikacija
headers = {
    "Authorization": f"Bearer {HF_TOKEN}",
    "Content-Type": "application/json"
}

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
EN_TOPICS = [
    "State governance, regional policy and public administration",
    "Environment, forests and climate change",
    "Energy",
    "Public finance",
    "Economic competitiveness and state information resources",
    "State security and defense",
    "Public security",
    "Culture",
    "Social security and employment",
    "Transportation and communications",
    "Health",
    "Education, science and sport",
    "Justice",
    "Foreign policy",
    "Land and food farming, rural development and fisheries"
]

def is_question_informative(q: str) -> bool:
        q = q.strip()
        if len(q) < 30:
            return False
        bendriniai = ["Įstatymas", "pakeitimas", "straipsnis", "projektas", "Nr.", "priedas", "XIV", "IX"]
        atitikimai = sum(1 for zodis in bendriniai if zodis.lower() in q.lower())
        if atitikimai >= 3 and len(q.split()) < 12:
            return False
        return True


def classify_with_api(question: str) -> str:
    if not is_question_informative(question):
        return "Nėra"

    try:
        translated_q = GoogleTranslator(source='lt', target='en').translate(question)
    except Exception as e:
        print(f"Vertimo į EN klaida: {e}")
        return "Vertimo klaida"

    prompt = f"""
    Question: {translated_q}
    Which of the following public policy topics best describes the question? Choose only one and answer ONLY with the topic name from the list below, no explanation.
    
    {chr(10).join(EN_TOPICS)}

    Topic:
    """

    try:
        response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=10)
        time.sleep(0.5)
        if response.status_code != 200:
            print(f"API klaida: {response.status_code}, {response.text}")
            return f"API klaida: {response.status_code}"
    except Exception as e:
        print(f"API užklausos klaida: {e}")
        return "API užklausos klaida"

    output = response.json()
    print("DEBUG API output:", output)

    result = output[0]["generated_text"].strip()
    if "Topic:" in result:
        answer_en = result.split("Topic:")[-1].strip().split("\n")[0]
    else:
        answer_en = result.split("\n")[-1].strip()


    topic_map = dict(zip(EN_TOPICS, TOPICS))
    if answer_en == "Unclear – not enough context":
        return "Neaišku – nepakanka informacijos"

    topic_map = dict(zip(EN_TOPICS, TOPICS))
    if answer_en in topic_map:
        return topic_map[answer_en]
    else:
        return "Neatpažinta tema"

    if answer_en not in topic_map:
        return "Neatpažinta tema"


def safe_classify(question: str) -> str:
    try:
        return classify_with_api(question)
    except Exception as e:
        print(f"Klaida apdorojant klausimą: {e}")
        return "Klasifikavimo klaida"


def classify_all_files_with_mistral(cleaned_dir: Path, classified_dir: Path):
    classified_dir.mkdir(parents=True, exist_ok=True)
    files = list(cleaned_dir.glob("*.csv"))
    print(f"Found {len(files)} files in '{cleaned_dir}'")

    for file in files:
        print(f"\n--- Now processing file: {file.name} ---")
        output_path = classified_dir / file.name

        df = pd.read_csv(file)
        if "question" not in df.columns:
            print(f"File {file.name} has no 'question' column, skipping.")
            continue

        df = df.dropna(subset=["question"])
        try:
            df["theme"] = df["question"].apply(safe_classify)
        except Exception as e:
            print(f"Error while classifying file {file.name}: {e}")

        df.to_csv(output_path, index=False)
        print(f"Saved: {output_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    cleaned = base_dir / "data" / "cleaned"
    classified = base_dir / "data" / "classified"
    classify_all_files_with_mistral(cleaned, classified)
