from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# Pagrindiniai konfigūracijos parametrai
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DB_PATH = Path(__file__).parent / "data" / "classified_questions.db"

# Duomenų bazės lentelės pavadinimas
TABLE_CLASSIFIED = "classified_questions"

# Duomenų bazės stulpelių pavadinimai
COL_DATE = "date"
COL_QUESTION = "question"
COL_THEME = "theme"

# Stulpelių vertimai į lietuvių kalbą
ALIASES = {
    COL_DATE: "data",
    COL_QUESTION: "klausimas",
    COL_THEME: "tema",
}
