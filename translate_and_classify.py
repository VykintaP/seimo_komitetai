import pandas as pd
from pathlib import Path
from transformers import pipeline
from deep_translator import GoogleTranslator
import logging
from functools import lru_cache

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

classifier = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

topics_en = [
    "Health",
    "Economy",
    "Regional policy",
    "Education",
    "Social policy",
    "Environment",
    "Security",
    "Governance",
    "Culture",
    "European Union",
    "Crisis management",
    "Ideological issues",
    "Justice and Legal affairs",
    "Infrastructure and Transport",
    "Technology and Digital policy",
    "Labour and Employment",
    "Public administration reform"
]

topics_lt = [
    "Sveikata",
    "Ekonomika",
    "Regionų politika",
    "Švietimas",
    "Socialinė politika",
    "Aplinkosauga",
    "Saugumas",
    "Valdymas",
    "Kultūra",
    "Europos Sąjunga",
    "Krizių valdymas",
    "Ideologiniai klausimai",
    "Teisingumas ir teisėkūra",
    "Infrastruktūra ir transportas",
    "Technologijos ir skaitmeninė politika",
    "Darbo rinka",
    "Viešojo valdymo reforma"
]

topic_dict = dict(zip(topics_en, topics_lt))

@lru_cache(maxsize=2048)
def translate_lt_to_en(text):
    try:
        return GoogleTranslator(source="lt", target="en").translate(text)
    except Exception as e:
        logging.warning(f"LT>EN vertimas nepavyko: {e}")
        return text

def classify_question(question_lt):
    q_en = translate_lt_to_en(question_lt)
    result = classifier(q_en, candidate_labels=topics_en)
    best_label_en = result["labels"][0]
    score = result["scores"][0]
    best_label_lt = topic_dict.get(best_label_en, "Nežinoma tema")
    return best_label_lt, score, q_en

def classify_dataframe(df):
    df = df[df["question"].notnull()].copy()
    df[["predicted_topic_lt", "confidence_score", "translated_question"]] = df["question"].apply(
        lambda q: pd.Series(classify_question(q))
    )
    return df

def classify_all_files(input_dir, output_dir):
    input_dir = Path(input_dir)
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    files = list(input_dir.glob("*.csv"))
    if not files:
        logging.warning(f"Nerasta jokių CSV failų kataloge: {input_dir}")
        return
    for file in files:
        df = pd.read_csv(file)
        if "question" not in df.columns:
            logging.warning(f"'question' stulpelis nerastas faile {file.name} – praleidžiama")
            continue
        if "committee" not in df.columns:
            df["committee"] = file.stem
        df_classified = classify_dataframe(df)
        output_path = output_dir / file.name
        df_classified.to_csv(output_path, index=False, encoding="utf-8")
        logging.info(f"Išsaugota: {output_path}")

if __name__ == "__main__":
    classify_all_files("data/cleaned", "data/classified")



