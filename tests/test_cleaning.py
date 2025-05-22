import pandas as pd
from pathlib import Path
from processing.cleaning_pipeline import clean_all_raw_files, clean_question
import shutil
from processing.cleaning_pipeline import extract_project_id


def test_clean_question_spaces():
    raw = "   Čia   yra \n    klausimas.  "
    cleaned = clean_question(raw)
    assert cleaned == "Čia yra klausimas."

def test_project_id_extraction():
    text = "Svarstomas Projektas Nr. XII-1234 ir Įstatymo projektas Nr. IX-456"
    result = extract_project_id(text)
    assert result == "XII-1234; IX-456"


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

    clean_all_raw_files(input_dir=raw_dir, output_dir=cleaned_dir, log_dir=metadata_dir)

    output_file = cleaned_dir / "test_committee_clean.csv"
    assert output_file.exists()

    df = pd.read_csv(output_file)
    assert len(df) == 1
    assert "Svarstomas klausimas" in df["question"].iloc[0]

    log_file = metadata_dir / "cleaning_log.json"
    assert log_file.exists()
    assert "project_id" in df.columns
    assert pd.isna(df["project_id"].iloc[0]) or isinstance(df["project_id"].iloc[0], str)

    log_file = metadata_dir / "cleaning_log.json"
    assert log_file.exists()