from scraper.scraper import run_scraper
from processing.cleaning_pipeline import clean_all_raw_files
from processing.classify import classify_all_cleaned_files
from pathlib import Path

RAW_DIR = Path("data/raw")
CLEANED_DIR = Path("data/cleaned")

def check_dir_nonempty(path, label):
    files = list(path.glob("*.csv"))
    if not files:
        print(f"[STOP] No {label} CSV files found in {path}")
        return False
    print(f"[OK] Found {len(files)} {label} CSV files in {path}")
    return True

if __name__ == "__main__":
    print("🔹 Scraping...")
    run_scraper()

    if not check_dir_nonempty(RAW_DIR, "raw"):
        exit(1)

    print("🔹 Cleaning...")
    clean_all_raw_files()

    if not check_dir_nonempty(CLEANED_DIR, "cleaned"):
        exit(1)

    print("🔹 Classifying...")
    classify_all_cleaned_files()

    print("✅ Pipeline finished successfully.")
