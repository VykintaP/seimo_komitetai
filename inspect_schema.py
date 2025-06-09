"""Spausdina duomenų bazės lentelės schemą."""

import sqlite3

import pandas as pd

from config import DB_PATH, TABLE_CLASSIFIED


def main():
    # Prisijungiam prie DB ir nuskaitom lentelės struktūrą
    conn = sqlite3.connect(DB_PATH)
    schema = pd.read_sql_query(f"PRAGMA table_info({TABLE_CLASSIFIED})", conn)
    conn.close()
    print("Lentelės schema:\n", schema.to_string(index=False))


if __name__ == "__main__":
    main()
