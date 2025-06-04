from pathlib import Path

DB_PATH = Path(__file__).parent / "data" / "classified_questions.db"

TABLE_CLASSIFIED = "classified_questions"

COL_DATE      = "date"
COL_QUESTION  = "question"
COL_THEME     = "theme"

ALIASES = {
    COL_DATE:     "data",
    COL_QUESTION: "klausimas",
    COL_THEME:    "tema",
}
