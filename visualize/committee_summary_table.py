import pandas as pd
import sqlite3
from dash import html, dcc, dash_table

from pathlib import Path

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "classified_questions.db"

def get_committee_summary_component():
    conn = sqlite3.connect(DB_PATH)
    query = """
        SELECT
            komitetas,
            COUNT(*) AS klausimai,
            COUNT(DISTINCT data) AS unikalios_datos,
            ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT data), 2) AS vid_klausimu_per_poseidi
        FROM classified_questions
        GROUP BY komitetas
        ORDER BY klausimai DESC
    """
    df = pd.read_sql_query(query, conn)
    conn.close()

    df = df.rename(columns={
        "komitetas": "Komitetas",
        "klausimai": "Klausimų sk.",
        "unikalios_datos": "Unikalios datos",
        "vid_klausimu_per_poseidi": "Vid. klausimų / posėdį"
    })

    return html.Div([
        html.H3("Komitetų veiklos santrauka", style={"color": "#2C3E50"}),
        dash_table.DataTable(
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
            style_table={"overflowX": "auto"},
            style_cell={"padding": "5px", "textAlign": "left"},
            style_header={"backgroundColor": "#F5F7FA", "fontWeight": "bold"},
        )
    ])
