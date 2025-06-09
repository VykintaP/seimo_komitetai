# visualize/utils/db.py

import sqlite3

import pandas as pd

from config import DB_PATH


def query_df(sql: str, params: tuple = ()) -> pd.DataFrame:
    """
    Vykdo SQL užklausą prieš SQLite duomenų bazę ir grąžina rezultatą kaip DataFrame.

    Args:
        sql (str): SQL užklausa, pvz., "SELECT * FROM table WHERE x = ?"
        params (tuple): Parametrai užklausos vietiniams laukams (naudojant ?)

    Returns:
        pd.DataFrame: Užklausos rezultatai kaip pandas DataFrame
    """
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn, params=params)
