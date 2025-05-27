import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from processing.scraper import run_scraper
from ml_pipeline.mistral_api_classifier import classify_with_api
from processing.cleaning_pipeline import clean_all_raw_files
from pathlib import Path



RAW_DIR = Path("darbotvarkiu_analize/data/raw")
CLEANED_DIR = Path("darbotvarkiu_analizedata/cleaned")
CLASSIFIED_DIR = Path("darbotvarkiu_analizedata/classified")
# TRAINING_DATA = Path("data/training_data.csv")

def check_dir_nonempty(path, label):
    files = list(path.glob("*.csv"))
    if not files:
        print(f"[STOP] No {label} CSV files found in {path}")
        return False
    print(f"[OK] Found {len(files)} {label} CSV files in {path}")
    return True

# def generate_training_data():
#     print("Generating training data...")
#     df = generate_data_from_classified(CLASSIFIED_DIR, TRAINING_DATA)
#     print(f"[OK] Saved training data to {TRAINING_DATA} ({len(df)} rows)")
#
# def train_model():
#     print("Training classifier...")
#     logreg_train_model()

if __name__ == "__main__":
    print("Step 1: Scraping")
    run_scraper()

    if not check_dir_nonempty(RAW_DIR, "raw"):
        exit(1)

    print("Step 2: Cleaning")
    clean_all_raw_files(RAW_DIR, CLEANED_DIR, Path("darbotvarkiu_analize/data/metadata"))

    if not check_dir_nonempty(CLEANED_DIR, "cleaned"):
        exit(1)

    print("Step 3: Classifying")
    classify_with_api (CLEANED_DIR, CLASSIFIED_DIR)


    if not check_dir_nonempty(CLASSIFIED_DIR, "classified"):
        exit(1)

    # print("Step 4: Generating training data")
    # generate_training_data()
    #
    # print("Step 5: Training model")
    # train_model()

    print("Pipeline finished successfully.")
