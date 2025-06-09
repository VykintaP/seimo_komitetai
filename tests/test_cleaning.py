from pathlib import Path

import pandas as pd

from processing import cleaning_pipeline
from processing.cleaning_pipeline import clean_file, clean_text


def test_clean_text_removes_symbols():
    """Tikrina ar clean_text() pašalina nereikalingus simbolius"""
    raw = "- Informacija \n apie projektą\xa0 "
    result = clean_text(raw)
    result = " ".join(result.split())
    assert result == "- Informacija apie projektą"


def test_clean_file_removes_garbage():
    """Tikrina ar clean_file() išvalo CSV failo turinį"""
    # Sudaromas testinis DataFrame 
    df = pd.DataFrame(
        {
            "date": ["2024-01-01"],
            "question": ["Labai svarbus klausimas dėl įstatymo"],
            "committee": ["Aplinkos apsaugos komitetas"],
            "project": ["XIIIP-1234"],
            "responsible": ["Jonas Jonaitis"],
            "attendees": ["Vardenis Pavardenis"],
        }
    )

    # Sukuriamas testinis failas
    test_input = Path("tests/data/test_input.csv")
    test_input.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(test_input, index=False)

    clean_file(test_input)

    out_file = cleaning_pipeline.CLEANED_DIR / test_input.name
    assert out_file.exists()  # Tikriname ar išvalytas failas sukurtas

    cleaned_df = pd.read_csv(out_file)
    expected_columns = [
        "date",
        "committee",
        "question",
        "project",
        "responsible",
        "attendees",
    ]
    assert set(expected_columns).issubset(cleaned_df.columns)
    assert len(cleaned_df) == 1

    # Išvalomi testiniai failai
    out_file.unlink()
    test_input.unlink()
