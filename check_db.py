import sqlite3
from pathlib import Path

DB_PATH = Path("data") / "classified_questions.db"

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# Parodo lenteles
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Lentelės duomenų bazėje:")
for t in tables:
    print("   -", t[0])

# Patikrina, ar yra reikalingi stulpeliai lentelėje classified_questions
cursor.execute("PRAGMA table_info(classified_questions);")
columns = [row[1] for row in cursor.fetchall()]
required = {'komitetas', 'tema', 'klausimas', 'data'}
missing = required - set(columns)

if missing:
    print(f"[ERROR] Trūksta stulpelių: {missing}")
else:
    print("[OK] Visi reikalingi stulpeliai yra.")

conn.close()
