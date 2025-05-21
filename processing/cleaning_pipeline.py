import pandas as pd
import re
from pathlib import Path
import json
from unidecode import unidecode



RAW_DIR = Path(__file__).resolve().parents[1] / "data" / "raw"
CLEANED_DIR = Path(__file__).resolve().parents[1] / "data" / "cleaned"
METADATA_DIR = Path(__file__).resolve().parents[1] / "data" / "metadata"
LOG_FILE = METADATA_DIR / "cleaning_log.json"
print(CLEANED_DIR)

CLEANED_DIR.mkdir(parents=True, exist_ok=True)
METADATA_DIR.mkdir(parents=True, exist_ok=True)

def clean_question(text: str) -> str:
    text = re.sub(r"\s+", " ", text).strip()
    return text

def clean_all_raw_files():
    log = []

    for file in RAW_DIR.glob("*.csv"):
        try:
            print(f"Processing: {file.name}")
            df = pd.read_csv(file)
            initial_count = len(df)
            issues = 0
            cleaned_rows = []

            for _, row in df.iterrows():
                question = str(row.get("question", "")).strip()
                cleaned = clean_question(question)

                print(">", question, "|", cleaned, "|", len(cleaned.split()))

                if not cleaned or len(cleaned.split()) < 2:
                    issues += 1
                    log.append({"file": file.name, "original": question, "issue": "too short or empty"})
                    continue

                date = row.get("date")
                committee = row.get("committee")

                cleaned_rows.append({
                    "date": date,
                    "committee": committee,
                    "question": cleaned,

                })

            cleaned_df = pd.DataFrame(cleaned_rows)
            out_name = unidecode(file.stem.lower().replace(" ", "_")) + "_clean.csv"
            cleaned_df.to_csv(CLEANED_DIR / out_name, index=False, encoding="utf-8")
            print(f"Saved: {out_name}")

            log.append({
                "file": file.name,
                "input_rows": initial_count,
                "output_rows": len(cleaned_df),
                "removed_rows": issues
            })

        except Exception as e:
            log.append({"file": file.name, "error": str(e)})


    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print(f"Cleaning finished. {len(log)} entries logged in {LOG_FILE}")

if __name__ == "__main__":
    clean_all_raw_files()
