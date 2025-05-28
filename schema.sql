CREATE TABLE IF NOT EXISTS classified_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    komitetas TEXT NOT NULL,
    data TEXT,
    klausimas TEXT NOT NULL,
    tema TEXT,
    vertimas_en TEXT,
    tikslumo_įvertis REAL
);
