import sqlite3
import pandas as pd
from pathlib import Path
import logging
logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parents[1]
CLASSIFIED_DIR = BASE_DIR / "data" / "classified"
DB_PATH = BASE_DIR / "data" / "classified_questions.db"
SCHEMA_PATH = BASE_DIR / "scripts" / "schema.sql"

RENAME_MAP = {
            "date": "data",
            "question": "klausimas",
            "theme": "tema",
            "committee": "komitetas",
            "project": "projektas",
            "responsible": "atsakingi",
            "attendees": "dalyviai"
        }
def main():
    logging.debug (f"[DEBUG] Looking for CSV files in: {CLASSIFIED_DIR.resolve()}")
    logging.debug (f"[DEBUG] Found files: {[f.name for f in CLASSIFIED_DIR.glob('*.csv')]}")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        cursor.executescript(f.read())

    all_dfs = []

    for file in CLASSIFIED_DIR.glob("*.csv"):
        komitetas = file.stem
        df = pd.read_csv(file)
        expected = set(RENAME_MAP.keys())
        missing = expected - set(df.columns)
        if missing:
            logger.warning(f"[SKIPPED] {file.name} – trūksta {missing}")
            continue

        if not set(RENAME_MAP.keys()).issubset(df.columns):
            print(f"[SKIPPED] {file.name} – missing columns: {set(RENAME_MAP) - set(df.columns)}")
            continue

        df = df.rename(columns=RENAME_MAP)

        for col in ["projektas", "atsakingi", "dalyviai"]:
            if col not in df.columns:
                df[col] = None

        df = df[["komitetas", "data", "klausimas", "tema", "projektas", "atsakingi", "dalyviai"]]
        all_dfs.append(df)

    if all_dfs:
        full_df = pd.concat(all_dfs, ignore_index=True)

        # kiek temų neatpažinta
        unknown_count = (full_df["tema"] == "Neatpažinta tema").sum()
        total_count = len(full_df)
        percent = round(unknown_count / total_count * 100, 2) if total_count else 0

        logger.info(f"[INFO] Neatpažinta tema: {unknown_count} klausimų ({percent}%)")

        # Įrašyti į data/diagnostics katalogą
        diagnostics_dir = Path(__file__).resolve().parents[1] / "data" / "diagnostics"
        diagnostics_dir.mkdir(parents=True, exist_ok=True)
        out_path = diagnostics_dir / "classification_quality.csv"

        pd.DataFrame([{
            "total_questions": total_count,
            "unknown_theme_count": unknown_count,
            "unknown_theme_percent": percent
        }]).to_csv(out_path, index=False)

        logger.info(f"[INFO] Klasifikavimo kokybė išsaugota: {out_path}")

    else:
        logger.error("[STOP] Nei vienas failas nebuvo įkeltas – galbūt stulpeliai neatitiko struktūros?")
    full_df.to_sql(name="classified_questions", con=conn, index=False, if_exists="replace")
    logger.info(f"[INFO] Įrašyta {len(full_df)} klausimų į duomenų bazę: {DB_PATH}")

    conn.close()

if __name__ == "__main__":
    main()
