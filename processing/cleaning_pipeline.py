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

def extract_project_id(text: str) -> str:
    matches = re.findall(
        r"(?:Projekt(?:o|as)?\s+Nr\.?|Įstatymo\s+projektas\s+Nr\.?|Dokumento\s+Nr\.?|Nr\.)\s*([A-Z0-9\-\/]+)",
        text,
        flags=re.IGNORECASE
    )
    return "; ".join(matches) if matches else None




def clean_all_raw_files(raw_dir=RAW_DIR, cleaned_dir=CLEANED_DIR, metadata_dir=METADATA_DIR):
    cleaned_dir.mkdir(parents=True, exist_ok=True)
    metadata_dir.mkdir(parents=True, exist_ok=True)
    log = []

    for file in raw_dir.glob("*.csv"):
        try:
            print(f"Processing: {file.name}")
            df = pd.read_csv(file)
            initial_count = len(df)
            issues = 0
            cleaned_rows = []

            for _, row in df.iterrows():
                question = str(row.get("question", "")).strip()
                cleaned = clean_question(question)

                if not cleaned or len(cleaned.split()) < 2:
                    issues += 1
                    log.append({"file": file.name, "original": question, "issue": "too short or empty"})
                    continue

                date = row.get("date")
                committee = row.get("committee")
                project_id = extract_project_id(cleaned)

                cleaned_rows.append({
                    "date": date,
                    "committee": committee,
                    "question": cleaned,
                    "project_id": project_id
                })

            cleaned_df = pd.DataFrame(cleaned_rows)
            out_name = unidecode(file.stem.lower().replace(" ", "_")) + "_clean.csv"
            cleaned_df.to_csv(cleaned_dir / out_name, index=False, encoding="utf-8")
            print(f"Saved: {out_name}")

            log.append({
                "file": file.name,
                "input_rows": initial_count,
                "output_rows": len(cleaned_df),
                "removed_rows": issues
            })

        except Exception as e:
            log.append({"file": file.name, "error": str(e)})

    log_file = metadata_dir / "cleaning_log.json"
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, indent=2, ensure_ascii=False)

    print(f"Cleaning finished. {len(log)} entries logged in {log_file}")


if __name__ == "__main__":
    clean_all_raw_files()
