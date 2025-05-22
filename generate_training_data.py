from translate_and_classify import classify_question
import pandas as pd
from pathlib import Path

RAW_DIR = Path("data/raw")
OUT_PATH = Path("data/training_data.csv")

all_data = []

for file in RAW_DIR.glob("*.csv"):
    df = pd.read_csv(file)
    df = df[df["question"].notnull()]
    df[["topic", "confidence_score", "translated_question"]] = df["question"].apply(
        lambda q: pd.Series(classify_question(q))
    )
    all_data.append(df[["question", "translated_question", "topic", "confidence_score"]])

full_df = pd.concat(all_data, ignore_index=True)
full_df.to_csv(OUT_PATH, index=False, encoding="utf-8")
print(f"Saved {len(full_df)} rows to {OUT_PATH}")
