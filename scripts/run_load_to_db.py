from pathlib import Path
import pandas as pd
import sqlite3


BASE_DIR = Path(__file__).resolve().parents[1]
classified_dir = BASE_DIR / "data" / "classified"
db_path = BASE_DIR / "data" / "classified_questions.db"


conn = sqlite3.connect(db_path)
all_dfs = []

for file in classified_dir.glob("*.csv"):
    print(f"Įkeliamas: {file.name}")
    df = pd.read_csv(file)
    df["komitetas"] = file.stem
    all_dfs.append(df)

full_df = pd.concat(all_dfs, ignore_index=True)
full_df.to_sql("classified_questions", conn, if_exists="replace", index=False)
conn.close()

print(f"[OK] Įrašyta {len(full_df)} eilučių į {db_path.name}")
