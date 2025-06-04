from deep_translator import GoogleTranslator
from dotenv import load_dotenv
import re
import pandas as pd
from pathlib import Path
from openai import OpenAI
from collections import Counter

load_dotenv()
import os
print("[DEBUG] API KEY yra:", os.getenv("OPENAI_API_KEY")[:8], "...")
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


unmapped_subtopics = []
unmapped_details = []
unmapped_subtopics_counter = Counter()
quality_counter = Counter()

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

# Automatiškai sugeneruoti subtemas ir jų žemėlapį
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

# klasifikavimas
def classify_with_api(question: str) -> str:
    try:
        translated_q = GoogleTranslator(source='lt', target='en').translate(question)
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
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0,
        )

    except Exception as e:
        print(f"API užklausos klaida: {e}")
        return "API užklausos klaida"

    # print("GPT atsakymas:", response["choices"][0]["message"]["content"].strip())
    answer_subtopic = response.choices[0].message.content.strip().split("\n")[-1].strip()
    answer_subtopic = answer_subtopic.strip('"')
    if not answer_subtopic:
        print(f"[WARNING] GPT atsakymas tuščias – nėra subtemos")
        unmapped_subtopics.append("EMPTY")
        unmapped_subtopics_counter["EMPTY"] += 1
        unmapped_details.append((question, "EMPTY"))
        return "Neatpažinta tema"
    normalized_answer = answer_subtopic.lower()

    # 1. Tikrinam ar tai subtema
    if normalized_answer in SUBTOPIC_TO_TOPIC:
        return SUBTOPIC_TO_TOPIC[normalized_answer]

    # 2. Tikrinam ar tai pilnas temos pavadinimas
    for i, topic in enumerate(EN_TOPICS):
        if normalized_answer == topic.lower():
            return TOPICS[i]

    # 3. Tikrinam ar tai fragmentas, esantis kurioje nors temoje
    for i, topic in enumerate(EN_TOPICS):
        fragments = re.split(r",|and", topic.lower())
        fragments = [f.strip() for f in fragments]
        if normalized_answer in fragments:
            return TOPICS[i]

    # 4. Tikrinam ar tai pilna tema, bet modelis ją grąžino vietoj subtemos
    for i, topic in enumerate(EN_TOPICS):
        if answer_subtopic in topic.lower():
            print(f"[WARNING] Subtema neatpažinta, bet panašu į temą: \"{answer_subtopic}\" → {TOPICS[i]}")
            return TOPICS[i]

    # Jei niekas netinka – grąžinam kaip neatpažintą
    print(f"[WARNING] Neatpažinta subtema ar tema: \"{answer_subtopic}\"")
    unmapped_subtopics.append(answer_subtopic)
    unmapped_subtopics_counter[normalized_answer] += 1
    unmapped_details.append((question, answer_subtopic))
    return "Neatpažinta tema"

    #     retry_1 = retry_with_topics(translated_q)
    #     if retry_1 in TOPICS:
    #         return retry_1
    #
    #     retry_2 = retry_with_topics(translated_q, explain=True)
    #     if retry_2 in TOPICS:
    #         return retry_2
    #
    #     unmapped_subtopics.append(answer_subtopic)
    #     return "Neatpažinta tema"

    return SUBTOPIC_TO_TOPIC[answer_subtopic]




# def retry_with_topics(translated_q: str, explain: bool = False) -> str:
#     topic_str = "\n".join(EN_TOPICS)
#     prompt = f"""
#     Classify the following policy question into one of the topics listed below. Choose only one and respond with the topic name, no explanation:
#
#     {topic_str}
#
#     Question: {translated_q}
#
#     Topic:
#     """ if not explain else f"""
#     We were not able to classify the question earlier. Please try again.
#
#     Classify the following policy question into one of the topics listed below. Choose only one and respond with the topic name:
#
#     {topic_str}
#
#     Question: {translated_q}
#     Topic:
#     """
#     try:
#         response = requests.post(API_URL, headers=headers, json={"inputs": prompt}, timeout=10)
#         time.sleep(0.5)
#         if response.status_code != 200:
#             print(f"[RETRY] API klaida: {response.status_code}")
#             return "RETRY API klaida"
#     except Exception as e:
#         print(f"[RETRY] API užklausos klaida: {e}")
#         return "RETRY API klaida"
#
#     topic = result.split("\n")[-1].strip()
#     if topic in TOPICS:
#         return topic
#     return "Neatpažinta tema"


def safe_classify(question: str) -> str:
    try:
        tema = classify_with_api(question)
        quality_counter[tema] += 1  # ← BŪTINA
        if tema == "Neatpažinta tema":
            unmapped_details.append((question, "Neatpažinta tema"))
        return tema
    except Exception as e:
        print(f"Klaida apdorojant klausimą: {e}")
        return "Klasifikavimo klaida"



def classify_all_files_with_gpt(cleaned_dir: Path, classified_dir: Path, base_dir: Path):
    classified_dir.mkdir(parents=True, exist_ok=True)
    files = list(cleaned_dir.glob("*.csv"))
    print(f"Rasti {len(files)} failai '{cleaned_dir}'")

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

        print(f"Išsaugota: {output_path}")

    # --- Rezultatų įrašymas po visų failų ---
    diagnostics_dir = base_dir / "data" / "diagnostics"
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    # Klasifikavimo kokybės suvestinė
    out_path = diagnostics_dir / "classification_quality.csv"
    pd.DataFrame.from_dict(quality_counter, orient="index", columns=["count"]) \
        .sort_values("count", ascending=False) \
        .to_csv(out_path)
    print(f"Klasifikavimo kokybės santrauka išsaugota: {out_path}")

    # Neatpažintų klausimų sąrašas
    if unmapped_details:
        details_path = diagnostics_dir / "unmapped_subtopics.csv"
        pd.DataFrame(unmapped_details, columns=["question", "model_output"]) \
            .to_csv(details_path, index=False)
        print(f"Neatpažintų klausimų sąrašas išsaugotas: {details_path}")

    # Neatpažintų reikšmių santrauka
    if unmapped_subtopics_counter:
        summary_path = diagnostics_dir / "unmapped_subtopics_summary.csv"
        pd.DataFrame.from_dict(unmapped_subtopics_counter, orient="index", columns=["count"]) \
            .sort_values("count", ascending=False) \
            .to_csv(summary_path)
        print(f"Neatpažintų reikšmių santrauka išsaugota: {summary_path}")


if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parents[1]
    cleaned = base_dir / "data" / "cleaned"
    classified = base_dir / "data" / "classified"
    classify_all_files_with_gpt(cleaned, classified, base_dir)

