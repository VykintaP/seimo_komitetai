# config.py
from pathlib import Path

# 1) Bendras kelias iki duomenų bazės
DB_PATH = Path(__file__).parent / "data" / "classified_questions.db"

# 2) Vieningas lentelės vardas
TABLE_CLASSIFIED = "classified_questions"

# 3) Stulpelių alias’ai, jei DB schema skiriasi:
COL_DATE      = "date"      # originalus laukas DB
COL_QUESTION  = "question"
COL_THEME     = "theme"

# 4) (nebūtina) žemėlapis alias → lietuviški pavadinimai
ALIASES = {
    COL_DATE:     "data",
    COL_QUESTION: "klausimas",
    COL_THEME:    "tema",
}
