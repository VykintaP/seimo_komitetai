"""Skriptas išvalo ir apdoroja komitetų žodžius iš CSV failo."""

import re
import sys
from pathlib import Path

import pandas as pd

from processing.lemmatization import lemmatize_text

# Pridedame pagrindinį projekto katalogą į Python kelią
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Nuskaitome stop žodžius
STOPWORDS_PATH = Path(__file__).resolve().parents[1] / "stop_words_lt.txt"
with STOPWORDS_PATH.open(encoding="utf-8") as f:
    stopwords = set(line.strip().lower() for line in f)

# Nustatome kelią iki duomenų failų
BASE_DIR = Path(__file__).resolve().parents[1]
INPUT_PATH = BASE_DIR / "data" / "diagnostics" / "words_by_committee.csv"
OUTPUT_PATH = BASE_DIR / "data" / "diagnostics" / "words_by_committee_cleaned.csv"

# Nuskaitome pradinius duomenis
df = pd.read_csv(INPUT_PATH)

# Ištraukiame žodžius ir jų skaičius
rows = []
for _, row in df.iterrows():
    committee = row["komitetas"]
    text = str(row["dažniausi žodžiai"])
    # Ieškome žodžių su skaičiais skliausteliuose
    items = re.findall(r"(\w+)\s+\((\d+)\)", text)
    for word, count in items:
        rows.append({"committee": committee, "word": word.lower(), "count": int(count)})

df_words = pd.DataFrame(rows)

# Lemmatizuojame žodžius ir pašaliname tuščias reikšmes
df_words["lemma"] = df_words["word"].apply(lambda x: lemmatize_text(str(x), stopwords))
df_words = df_words.explode("lemma").dropna(subset=["lemma"])

# Grupuojame pagal komitetą ir lemą
grouped = df_words.groupby(["committee", "lemma"])["count"].sum().reset_index()
grouped = grouped.sort_values("count", ascending=False)

# Išsaugome rezultatus
grouped.to_csv(OUTPUT_PATH, index=False, encoding="utf-8")
print("[OK] Išvalyti duomenys išsaugoti:", OUTPUT_PATH.name)
