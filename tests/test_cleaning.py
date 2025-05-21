import pandas as pd
from pathlib import Path
from processing.cleaning_pipeline import clean_all_raw_files, clean_question
import shutil

def test_clean_question_spaces():
    raw = "   Čia   yra \n    klausimas.  "
    cleaned = clean_question(raw)
    assert cleaned == "Čia yra klausimas."

def test_clean_all_raw_files_creates_cleaned(tmp_path):
    raw_dir = tmp_path / "data" / "raw"
    cleaned_dir = tmp_path / "data" / "cleaned"
    metadata_dir = tmp_path / "data" / "metadata"
    raw_dir.mkdir(parents=True)
    cleaned_dir.mkdir(parents=True)
    metadata_dir.mkdir(parents=True)

    test_input = pd.DataFrame([
        {"date": "2025-05-21", "question": "Svarstomas klausimas dėl įstatymo", "committee": "Testo komitetas"},
        {"date": "2025-05-21", "question": "A", "committee": "Testo komitetas"}
    ])
    test_file = raw_dir / "test_committee.csv"
    test_input.to_csv(test_file, index=False)

    original_raw = Path(__file__).resolve().parents[1] / "data" / "raw"
    original_cleaned = Path(__file__).resolve().parents[1] / "data" / "cleaned"
    original_meta = Path(__file__).resolve().parents[1] / "data" / "metadata"

    shutil.rmtree(original_raw, ignore_errors=True)
    shutil.rmtree(original_cleaned, ignore_errors=True)
    shutil.rmtree(original_meta, ignore_errors=True)
    original_raw.mkdir(parents=True)
    original_cleaned.mkdir(parents=True)
    original_meta.mkdir(parents=True)

    shutil.copy(test_file, original_raw / test_file.name)

    clean_all_raw_files()

    output_file = original_cleaned / "test_committee_clean.csv"
    assert output_file.exists()
    df = pd.read_csv(output_file)
    assert len(df) == 1
    assert "Svarstomas klausimas" in df["question"].iloc[0]

    log_file = original_meta / "cleaning_log.json"
    assert log_file.exists()
