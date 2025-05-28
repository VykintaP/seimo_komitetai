import sqlite3
import pandas as pd
from pathlib import Path

CLASSIFIED_DIR = Path("data/classified")
DB_PATH = "classified_questions.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Sukuriame lentelę iš schema.sql (jei dar nėra)
with open("schema.sql", "r", encoding="utf-8") as f:
    cursor.executescript(f.read())

# Einame per visus CSV failus
for file in CLASSIFIED_DIR.glob("*.csv"):
    komitetas = file.stem  # failo vardas be .csv
    df = pd.read_csv(file)

    # Įsitikiname, kad yra reikiami stulpeliai
    if not {"date", "question", "topic", "translation_en", "score"}.issubset(df.columns):
        print(f"[SKIPPED] {file.name} – missing required columns")
        continue

    df["komitetas"] = komitetas
    df = df.rename(columns={
        "date": "data",
        "question": "klausimas",
        "topic": "tema",
        "translation_en": "vertimas_en",
        "score": "tikslumo_įvertis"
    })

    df[["komitetas", "data", "klausimas", "tema", "vertimas_en", "tikslumo_įvertis"]].to_sql(
        "classified_questions", conn, if_exists="append", index=False
    )

    print(f"[OK] {file.name} – {len(df)} įrašų įkelta")

conn.close()
