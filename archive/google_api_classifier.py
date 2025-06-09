import sqlite3
import time
from collections import Counter
from pathlib import Path

import pandas as pd
import requests
from deep_translator import GoogleTranslator

from config import DB_PATH

conn = sqlite3.connect(DB_PATH)
# TOKENAS


headers = {"Authorization": f"Bearer {HF_TOKEN}", "Content-Type": "application/json"}

# Valstybės veiklos sritys pagal LR Strateginio valdymo įstatymo 3 str. 26 dalį
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
    "Žemės ir maisto ūkis, kaimo plėtra ir žuvininkystė",
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
    "Land and food farming, rural development and fisheries",
]


# Automatiškai sugeneruoti subtemas
def extract_subtopics(topics: list[str]) -> tuple[list[str], dict[str, str]]:
    subtopics = set()
    subtopic_map = {}

    for topic in topics:

        fragments = topic.split(",")
        for frag in fragments:
            frag = frag.strip()

            if " and " in frag:
                parts = frag.split(" and ")
                for part in parts:
                    clean_part = part.strip().lower()
                    subtopics.add(clean_part)
                    subtopic_map[clean_part] = topic
            else:
                clean_frag = frag.strip().lower()
                subtopics.add(clean_frag)
                subtopic_map[clean_frag] = topic

    return sorted(subtopics), subtopic_map


EN_SUBTOPICS, SUBTOPIC_TO_TOPIC = extract_subtopics(EN_TOPICS)


# grąžina į temas atgal
def generate_subtopic_map(topics: list[str]) -> dict:
    mapping = {}
    for topic in topics:
        parts = [p.strip().lower() for p in topic.replace(",", "").split()]
        for word in parts:
            if word not in mapping:
                mapping[word] = topic
    return mapping


unmapped_subtopics = []


# klasifikavimas
def classify_with_api(question: str) -> str:
    if not is_question_informative(question):
        return "Nėra"

    try:
        translated_q = GoogleTranslator(source="lt", target="en").translate(question)
    except Exception as e:
        print(f"Vertimo į EN klaida: {e}")
        return "Vertimo klaida"

    subtopics_str = "\n".join(EN_SUBTOPICS)

    prompt = f"""
    You are a government policy analyst. Your job is to classify agenda items into policy subtopics.

    A policy agenda item is: {translated_q}
    
    Which of the following public policy subtopic best describes the question? Choose only one and answer ONLY with the subtopic from the list below, no explanation.

    # Subtopic:
    {chr(10).join(f'- "{t}"' for t in EN_SUBTOPICS)}
    
    Answer must exactly match one of the subtopics above.

    Answer:
    """

    try:
        response = requests.post(
            API_URL, headers=headers, json={"inputs": prompt}, timeout=10
        )
        time.sleep(0.5)
        if response.status_code != 200:
            print(f"API klaida: {response.status_code}, {response.text}")
            return f"API klaida: {response.status_code}"
    except Exception as e:
        print(f"API užklausos klaida: {e}")
        return "API užklausos klaida"

    output = response.json()
    print("DEBUG API:", output)

    result = output[0]["generated_text"].strip()

    answer_subtopic = result.split("\n")[-1].strip().lower()

    # Bandome dar kartą jei nesuklasifikuoja pirmu bandimu
    if answer_subtopic not in SUBTOPIC_TO_TOPIC:
        print(f"[WARNING] Neatpažinta subtema: {answer_subtopic}")

        retry_1 = retry_with_topics(translated_q)
        if retry_1 in TOPICS:
            return retry_1

        retry_2 = retry_with_topics(translated_q, explain=True)
        if retry_2 in TOPICS:
            return retry_2

        unmapped_subtopics.append(answer_subtopic)
        return "Neatpažinta tema"

    return SUBTOPIC_TO_TOPIC[answer_subtopic]


print(f"[WARNING] Neatpažinta subtema: {answer_subtopic}")


def retry_with_topics(translated_q: str, explain: bool = False) -> str:
    topic_str = "\n".join(EN_TOPICS)
    prompt = (
        f"""
    Classify the following policy question into one of the topics listed below. Choose only one and respond with the topic name, no explanation:

    {topic_str}

    Question: {translated_q}

    Topic:
    """
        if not explain
        else f"""
    We were not able to classify the question earlier. Please try again.

    Classify the following policy question into one of the topics listed below. Choose only one and respond with the topic name:

    {topic_str}

    Question: {translated_q}
    Topic:
    """
    )
    try:
        response = requests.post(
            API_URL, headers=headers, json={"inputs": prompt}, timeout=10
        )
        time.sleep(0.5)
        if response.status_code != 200:
            print(f"[RETRY] API klaida: {response.status_code}")
            return "RETRY API klaida"
    except Exception as e:
        print(f"[RETRY] API užklausos klaida: {e}")
        return "RETRY API klaida"

    output = response.json()
    result = output[0]["generated_text"].strip()
    topic = result.split("\n")[-1].strip()
    if topic in TOPICS:
        return topic
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
    print(f"Rasti {len(files)} failai '{cleaned_dir}'")
    quality_counter = Counter()

    for file in files:
        print(f"\n--- Apdorojamas failas: {file.name} ---")
        output_path = classified_dir / file.name

        df = pd.read_csv(file)
        if "question" not in df.columns:
            print(f"Failas {file.name} neturi 'klausimai' stulpelio, praleidžiama.")
            continue

        df = df.dropna(subset=["question"])
        try:
            df["theme"] = df["question"].apply(safe_classify)
        except Exception as e:
            print(f"Klaida klasifikuojant {file.name}: {e}")

        df.to_csv(output_path, index=False)
        quality_counter.update(df["theme"].value_counts().to_dict())

        print(f"Išsaugota: {output_path}")

        diagnostics_dir = base_dir / "data" / "diagnostics"
        diagnostics_dir.mkdir(parents=True, exist_ok=True)
        out_path = diagnostics_dir / "classification_quality.csv"
        pd.DataFrame.from_dict(
            quality_counter, orient="index", columns=["count"]
        ).sort_values("count", ascending=False).to_csv(out_path)
        print(f"Klasifikavimo kokybės santrauka išsaugota: {out_path}")

    if unmapped_subtopics:
        diagnostics_dir = base_dir / "data" / "diagnostics"
        diagnostics_dir.mkdir(parents=True, exist_ok=True)
        pd.Series(unmapped_subtopics).value_counts().to_csv(
            diagnostics_dir / "unmapped_subtopics.csv"
        )


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    cleaned = base_dir / "data" / "cleaned"
    classified = base_dir / "data" / "classified"
    classify_all_files_with_mistral(cleaned, classified)
