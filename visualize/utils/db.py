import sqlite3
import pandas as pd
from config import DB_PATH

def query_df(sql: str, params: tuple = ()) -> pd.DataFrame:
    with sqlite3.connect(DB_PATH) as conn:
        return pd.read_sql_query(sql, conn, params=params)
