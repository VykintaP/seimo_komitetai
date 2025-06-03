import pandas as pd
from pathlib import Path
from processing.cleaning_pipeline import clean_text, clean_file
from processing import cleaning_pipeline

def test_clean_text_removes_symbols():
    raw = "- Informacija \n apie projektą\xa0 "
    result = clean_text(raw)
    result = " ".join(result.split())
    assert result == "- Informacija apie projektą"

def test_clean_file_removes_garbage():
    df = pd.DataFrame({
        "date": ["2024-01-01"],
        "question": ["Labai svarbus klausimas dėl įstatymo"],
        "committee": ["Aplinkos apsaugos komitetas"],
        "project": ["XIIIP-1234"],
        "responsible": ["Jonas Jonaitis"],
        "attendees": ["Vardenis Pavardenis"]
    })

    test_input = Path("tests/data/test_input.csv")
    test_input.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(test_input, index=False)

    clean_file(test_input)

    out_file = cleaning_pipeline.CLEANED_DIR / test_input.name
    assert out_file.exists()  # įsitikinam, kad išvalytas failas sukurtas

    cleaned_df = pd.read_csv(out_file)
    expected_columns = ["date", "committee", "question", "project", "responsible", "attendees"]
    assert set(expected_columns).issubset(cleaned_df.columns)
    assert len(cleaned_df) == 1

    out_file.unlink()
    test_input.unlink()

