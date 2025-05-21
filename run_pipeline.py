from scraper.scraper import run_scraper
from processing.cleaning_pipeline import clean_all_raw_files
from processing.classify import classify_all_cleaned_files

if __name__ == "__main__":
    run_scraper()
    clean_all_raw_files()
    classify_all_cleaned_files()
