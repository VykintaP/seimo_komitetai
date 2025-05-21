import pandas as pd
import re

def normalize_question(text):
    if not isinstance(text, str):
        return ""

    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"^\d+\.\s*", "", text)
    text = re.sub(r"Nr\.[^\s]*", "", text)
    text = re.sub(r"[“”\"']", "", text)
    text = re.sub(r"\s{2,}", " ", text)


    if re.fullmatch(r"\(.*\)", text):
        return ""
    if re.search(r"(?i)(r\.|kab\.|kabineto|pos\.|posėdis|salėje)", text):
        return ""

    text = text.strip(",.:-; ")


    if len(text.split()) < 2:
        return ""

    return text



def clean_questions(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df["question"] = df["question"].apply(normalize_question)
    df = df[df["question"].str.strip() != ""]
    return df
