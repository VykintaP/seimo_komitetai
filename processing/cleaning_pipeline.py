import logging
from pathlib import Path

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Duomenų direktorijų struktūra 
BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
CLEANED_DIR = BASE_DIR / "data" / "cleaned"
CLEANED_DIR.mkdir(parents=True, exist_ok=True)

# Privalomi duomenų stulpeliai
REQUIRED_COLUMNS = {
    "date",
    "question",
    "committee",
    "project",
    "responsible",
    "attendees",
}

# Tekstiniai laukai, kuriems reikia valymo
TEXT_FIELDS = ["question", "responsible", "attendees"]


def clean_text(text):
    """Pašalina nereikalingus simbolius ir perteklinius tarpus"""
    return (
        str(text)
        .replace("\xa0", " ")
        .replace("•", "-")
        .replace("●", "-")
        .replace("–", "-")
        .replace("\n", " ")
        .strip()
    )


def clean_file(file_path: Path):
    """Išvalo duomenis iš CSV failo ir išsaugo rezultatus"""
    df = pd.read_csv(file_path)

    # Tekstinių laukų valymas
    for col in TEXT_FIELDS:
        df[f"cleaned_{col}"] = (
            df[col]
            .fillna("")
            .astype(str)
            .str.replace(r"\s+", " ", regex=True)
            .apply(clean_text)
        )
        # Atmesti klausimus, kurie per trumpi arba be turinio
        df = df[df["cleaned_question"].str.len() > 10]
        df = df[
            ~df["cleaned_question"]
            .str.lower()
            .str.strip()
            .isin(["", "none", "nan", "nėra", "informacija", "papildoma medžiaga"])
        ]

    output_columns = [
        "date",
        "committee",
        "question",
        "project",
        "responsible",
        "attendees",
    ]
    out_path = CLEANED_DIR / file_path.name
    df[output_columns].to_csv(out_path, index=False, encoding="utf-8")
    logging.info(f"[{file_path.name}] Išsaugota {len(df)} klausimų -> {out_path}")


def run_cleaning():
    """Apdoroja visus RAW_DIR kataloge esančius CSV failus"""
    files = list(RAW_DIR.glob("*.csv"))
    if not files:
        logging.warning(f"Nėra failų {RAW_DIR}")
        return

    for file_path in files:
        try:
            clean_file(file_path)
        except Exception as e:
            logging.error(f"Klaida - {file_path.name}: {e}")


if __name__ == "__main__":
    run_cleaning()
