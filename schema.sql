CREATE TABLE IF NOT EXISTS classified_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    komitetas TEXT,
    data TEXT,
    klausimas TEXT,
    tema TEXT,
    project_id TEXT,
    responsible_actor TEXT,
    invited_presenters TEXT
);
