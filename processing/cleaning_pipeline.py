import pandas as pd
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def clean_question(text):
    if not isinstance(text, str):
        return None
    text = text.strip()
    if len(text) < 15:
        return None
    return text

def clean_all_raw_files(raw_dir: Path, cleaned_dir: Path, metadata_dir: Path = None):
    raw_dir = Path(raw_dir)
    cleaned_dir = Path(cleaned_dir)
    cleaned_dir.mkdir(parents=True, exist_ok=True)

    files = list(raw_dir.glob("*.csv"))
    if not files:
        logging.warning(f"No raw CSV files found in {raw_dir}")
        return

    for file in files:
        try:
            df = pd.read_csv(file)
        except Exception as e:
            logging.warning(f"Failed to read {file.name}: {e}")
            continue

        if df.empty or "question" not in df.columns:
            logging.warning(f"Skipping {file.name} – no 'question' column or empty file.")
            continue

        cleaned_rows = []
        for _, row in df.iterrows():
            question = clean_question(row.get("question", ""))
            if question:
                cleaned_rows.append({
                    "date": row.get("date"),
                    "question": question,
                    "committee": row.get("committee"),
                    "project_id": row.get("project_id"),
                    "responsible_actor": row.get("responsible_actor"),
                    "invited_presenters": row.get("invited_presenters"),
                })

        if cleaned_rows:
            df_cleaned = pd.DataFrame(cleaned_rows)
            cleaned_path = cleaned_dir / file.name
            df_cleaned.to_csv(cleaned_path, index=False, encoding="utf-8")
            logging.info(f"Saved {len(df_cleaned)} rows to {cleaned_path}")
        else:
            logging.warning(f"No valid questions in {file.name}")
