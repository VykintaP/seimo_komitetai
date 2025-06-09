import os
import sqlite3
import sys
from pathlib import Path

import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ml_pipeline.classify_with_gpt_api import classify_all_files_with_gpt
from processing.cleaning_pipeline import run_cleaning
from processing.scraper import run_scraper

# Pagrindiniai sistemos katalogai
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLASSIFIED_DIR = BASE_DIR / "data" / "classified"
METADATA_DIR = BASE_DIR / "data" / "metadata"


def check_dir_nonempty(path, label):
    """Patikrina ar kataloge yra CSV failų"""
    files = list(path.glob("*.csv"))
    if not files:
        print(f"[STOP] Nei vieno {label} CSV nėra {path}")
        return False
    print(f"[OK] {len(files)} {label} CSV failai yra {path}")
    return True


def load_cleaned_to_db(cleaned_dir, db_path):
    """Sukelia išvalytus failus į SQLite duomenų bazę"""
    conn = sqlite3.connect(db_path)
    all_dfs = []
    # Nuskaitome visus CSV failus
    for file in cleaned_dir.glob("*.csv"):
        df = pd.read_csv(file)
        df["komitetas"] = file.stem
        all_dfs.append(df)
    # Sujungiame į vieną DataFrame
    full_df = pd.concat(all_dfs, ignore_index=True)
    full_df.to_sql("cleaned_questions", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[OK] Užkrautos {len(full_df)} eilutės į {db_path.name} (cleaned_questions)")


if __name__ == "__main__":
    # Vykdome duomenų apdorojimo etapus
    print("1. Nuskaitymas")
    run_scraper()

    if not check_dir_nonempty(RAW_DIR, "raw"):
        exit(1)

    print("2. Valymas")
    run_cleaning()

    if not check_dir_nonempty(CLEANED_DIR, "cleaned"):
        exit(1)

    print("3. Klasifikavimas")
    classify_all_files_with_gpt(CLEANED_DIR, CLASSIFIED_DIR, BASE_DIR)

    if not check_dir_nonempty(CLASSIFIED_DIR, "classified"):
        exit(1)

    print("4. Įrašoma į duomenų bazę")
    from scripts.load_to_sql import main as load_to_sql

    load_to_sql()

    DB_PATH = BASE_DIR / "data" / "classified_questions.db"
    load_cleaned_to_db(CLEANED_DIR, DB_PATH)

    print("[PABAIGA] Sėkmingai užbaigta.")
