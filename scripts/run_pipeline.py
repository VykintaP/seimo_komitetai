import sys
import os
from pathlib import Path
import pandas as pd
import sqlite3

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from processing.scraper import run_scraper
from processing.cleaning_pipeline import run_cleaning
from ml_pipeline.classify_with_gpt_api import classify_all_files_with_gpt


BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLASSIFIED_DIR = BASE_DIR / "data" / "classified"
METADATA_DIR = BASE_DIR / "data" / "metadata"

""" 
Patikrina ar yra csv 
"""
def check_dir_nonempty(path, label):
    files = list(path.glob("*.csv"))
    if not files:
        print(f"[STOP] Nei vieno {label} CSV nėra {path}")
        return False
    print(f"[OK] {len(files)} {label} CSV failai yra {path}")
    return True

"""
Executes pipeline steps:

1. Scrape committee agendas from the Seimas website (lrs.lt)
2. Clean raw text data
3. Classify questions into public policy topics using Mistal API
4. Write results to a SQLite database
"""


def load_cleaned_to_db(cleaned_dir, db_path):
    conn = sqlite3.connect(db_path)
    all_dfs = []
    for file in cleaned_dir.glob("*.csv"):
        df = pd.read_csv(file)
        df["komitetas"] = file.stem
        all_dfs.append(df)
    full_df = pd.concat(all_dfs, ignore_index=True)
    full_df.to_sql("cleaned_questions", conn, if_exists="replace", index=False)
    conn.close()
    print(f"[OK] Uploaded {len(full_df)} rows to {db_path.name} (cleaned_questions)")

if __name__ == "__main__":
    print("Step 1: Scraping")
    run_scraper()

    if not check_dir_nonempty(RAW_DIR, "raw"):
        exit(1)

    print("Step 2: Cleaning")
    run_cleaning()

    if not check_dir_nonempty(CLEANED_DIR, "cleaned"):
        exit(1)

    print("Step 3: Classifying")
    classify_all_files_with_gpt(CLEANED_DIR, CLASSIFIED_DIR, BASE_DIR)


    if not check_dir_nonempty(CLASSIFIED_DIR, "classified"):
        exit(1)

    print("Step 4: Writing classified data to database")
    from scripts.load_to_sql import main as load_to_sql
    load_to_sql()

    print("Step 5: Writing cleaned questions to database")
    DB_PATH = BASE_DIR / "data" / "classified_questions.db"
    load_cleaned_to_db(CLEANED_DIR, DB_PATH)

    print("[DONE] Finished successfully.")
