import sqlite3
import pandas as pd
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[1]
CLASSIFIED_DIR = BASE_DIR / "data" / "classified"
DB_PATH = BASE_DIR / "data" / "classified_questions.db"
SCHEMA_PATH = BASE_DIR / "scripts" / "schema.sql"

def main():
    print(f"[DEBUG] Looking for CSV files in: {CLASSIFIED_DIR.resolve()}")
    print(f"[DEBUG] Found files: {[f.name for f in CLASSIFIED_DIR.glob('*.csv')]}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    all_dfs = []

    for file in CLASSIFIED_DIR.glob("*.csv"):
        komitetas = file.stem
        df = pd.read_csv(file)

        if "committee" not in df.columns:
            df["committee"] = komitetas

        RENAME_MAP = {
            "date": "data",
            "question": "klausimas",
            "theme": "tema",
            "committee": "komitetas",
            "projektas": "projektas",
            "atsakingi": "atsakingi",
            "dalyviai": "dalyviai"
        }

        if not set(RENAME_MAP.keys()).issubset(df.columns):
            print(f"[SKIPPED] {file.name} – missing columns: {set(RENAME_MAP) - set(df.columns)}")
            continue

        df = df.rename(columns=RENAME_MAP)

        for col in ["projektas", "atsakingi", "dalyviai"]:
            if col not in df.columns:
                df[col] = None

        df = df[["komitetas", "data", "klausimas", "tema", "projektas", "atsakingi", "dalyviai"]]
        all_dfs.append(df)

    if all_dfs:
        full_df = pd.concat(all_dfs, ignore_index=True)

        # kiek temų neatpažinta
        unknown_count = (full_df["tema"] == "Neatpažinta tema").sum()
        total_count = len(full_df)
        percent = round(unknown_count / total_count * 100, 2) if total_count else 0

        print(f"[INFO] Neatpažinta tema: {unknown_count} klausimų ({percent}%)")

        # Įrašyti į data/diagnostics katalogą
        diagnostics_dir = Path(__file__).resolve().parents[1] / "data" / "diagnostics"
        diagnostics_dir.mkdir(parents=True, exist_ok=True)
        out_path = diagnostics_dir / "classification_quality.csv"

        pd.DataFrame([{
            "total_questions": total_count,
            "unknown_theme_count": unknown_count,
            "unknown_theme_percent": percent
        }]).to_csv(out_path, index=False)

        print(f"[INFO] Klasifikavimo kokybė išsaugota: {out_path}")

    else:
        print("[STOP] Nei vienas failas nebuvo įkeltas – galbūt stulpeliai neatitiko struktūros?")

    conn.close()

if __name__ == "__main__":
    main()
