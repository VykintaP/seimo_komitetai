from scraper.scraper import run_scraper
from processing.cleaning_pipeline import clean_all_raw_files
from translate_and_classify import classify_all_files
from pathlib import Path
import subprocess
import pandas as pd

RAW_DIR = Path("data/raw")
CLEANED_DIR = Path("data/cleaned")
CLASSIFIED_DIR = Path("data/classified")
TRAINING_DATA = Path("data/training_data.csv")

def check_dir_nonempty(path, label):
    files = list(path.glob("*.csv"))
    if not files:
        print(f"[STOP] No {label} CSV files found in {path}")
        return False
    print(f"[OK] Found {len(files)} {label} CSV files in {path}")
    return True

def generate_training_data():
    print("Generating training data...")
    from generate_training_data import all_data
    full_df = pd.concat(all_data, ignore_index=True)
    full_df.to_csv(TRAINING_DATA, index=False, encoding="utf-8")
    print(f"[OK] Saved training data to {TRAINING_DATA}")

def train_model():
    print("Training classifier...")
    subprocess.run(["python", "train_classifier.py"], check=True)

if __name__ == "__main__":
    print("Step 1: Scraping")
    run_scraper()

    if not check_dir_nonempty(RAW_DIR, "raw"):
        exit(1)

    print("Step 2: Cleaning")
    clean_all_raw_files()

    if not check_dir_nonempty(CLEANED_DIR, "cleaned"):
        exit(1)

    print("Step 3: Classifying")
    classify_all_files(CLEANED_DIR, CLASSIFIED_DIR)

    if not check_dir_nonempty(CLASSIFIED_DIR, "classified"):
        exit(1)

    print("Step 4: Generating training data")
    generate_training_data()

    print("Step 5: Training model")
    train_model()

    print("Pipeline finished successfully.")
