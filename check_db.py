import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "classified_questions.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print("Lentelės duomenų bazėje:")
for t in tables:
    print("   -", t[0])

conn.close()
