import sys
import os
from pathlib import Path

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from processing.scraper import run_scraper
from ml_pipeline.mistral_api_classifier import classify_with_api
from processing.cleaning_pipeline import clean_all_raw_files

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLASSIFIED_DIR = BASE_DIR / "data" / "classified"
METADATA_DIR = BASE_DIR / "data" / "metadata"

def check_dir_nonempty(path, label):
    files = list(path.glob("*.csv"))
    if not files:
        print(f"[STOP] No {label} CSV files found in {path}")
        return False
    print(f"[OK] Found {len(files)} {label} CSV files in {path}")
    return True

if __name__ == "__main__":
    print("Step 1: Scraping")
    run_scraper()

    if not check_dir_nonempty(RAW_DIR, "raw"):
        exit(1)

    print("Step 2: Cleaning")
    clean_all_raw_files(RAW_DIR, CLEANED_DIR, METADATA_DIR)

    if not check_dir_nonempty(CLEANED_DIR, "cleaned"):
        exit(1)

    print("Step 3: Classifying")
    classify_with_api(CLEANED_DIR, CLASSIFIED_DIR)

    if not check_dir_nonempty(CLASSIFIED_DIR, "classified"):
        exit(1)

    print("Pipeline finished successfully.")
