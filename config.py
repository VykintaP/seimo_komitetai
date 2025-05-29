# config.py
"""
Centralūs projektų parametrai: DB failas ir lentelių vardai.
"""
# kelias iki sqlite DB
DB_PATH = "data/classified_questions.db"

# lentelei, kurioje saugome visą klasifikacijos rezultatą
TABLE_CLASSIFIED = "classified_questions"

# (priešingiems atvejams: diagnostikos ataskaitoms ar pan.)
TABLE_DIAGNOSTICS = "data_quality_reports"
