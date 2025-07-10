-- Lentelė saugo klasifikuotų komitetų posėdžių klausimų duomenis
CREATE TABLE IF NOT EXISTS classified_questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    komitetas TEXT,  # Komiteto pavadinimas 
    data TEXT,  # Posėdžio data
    klausimas TEXT,  # Svarstomo klausimo tekstas
    tema TEXT,  # Priskirta tematika
    projektas TEXT,  # Svarstomo projekto numeris
    atsakingi TEXT,  # Atsakingi asmenys
    dalyviai TEXT  # Kviesti dalyvauti asmenys
);