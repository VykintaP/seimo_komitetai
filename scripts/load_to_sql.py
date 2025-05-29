import sqlite3
import pandas as pd
from pathlib import Path

def main():
    CLASSIFIED_DIR = Path(__file__).resolve().parents[1] / "data" / "classified"
    DB_PATH = Path(__file__).resolve().parents[1] / "classified_questions.db"
    SCHEMA_PATH = Path(__file__).resolve().parent.parent / "schema.sql"

    print(f"[DEBUG] Looking for CSV files in: {CLASSIFIED_DIR.resolve()}")
    print(f"[DEBUG] Found files: {[f.name for f in CLASSIFIED_DIR.glob('*.csv')]}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    for file in CLASSIFIED_DIR.glob("*.csv"):
        komitetas = file.stem  # failo vardas be .csv
        df = pd.read_csv(file)

        # Pridedam 'committee' jei jo nėra
        if "committee" not in df.columns:
            df["committee"] = komitetas

        RENAME_MAP = {
            "date": "data",
            "question": "klausimas",
            "theme": "tema",
            "committee": "komitetas",
        }

        required_cols = set(RENAME_MAP.keys())
        if not required_cols.issubset(df.columns):
            print(f"[SKIPPED] {file.name} – missing columns: {required_cols - set(df.columns)}")
            print(f"[DEBUG] Available columns: {df.columns.tolist()}")
            continue

        df = df.rename(columns=RENAME_MAP)

        columns_to_insert = ["komitetas", "data", "klausimas", "tema"]
        for col in ["project_id", "responsible_actor", "invited_presenters"]:
            if col in df.columns:
                columns_to_insert.append(col)

        df[columns_to_insert].to_sql(
            "classified_questions", conn, if_exists="replace", index=False
        )

        print(f"[OK] {file.name} – {len(df)} įrašų įkelta")

    conn.close()

if __name__ == "__main__":
    main()
