import pandas as pd
import plotly.express as px
import sqlite3
from pathlib import Path
from dash import html, dcc

def get_theme_area_layout():
    db_path = Path(__file__).resolve().parents[1] / "classified_questions.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT data, komitetas FROM classified_questions", conn)
    conn.close()

    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    df = df.dropna(subset=["data", "komitetas"])
    df["month"] = df["data"].dt.to_period("M").dt.to_timestamp()

    trend_df = df.groupby(["month", "komitetas"]).size().reset_index(name="klausimų skaičius")

    fig = px.line(
        trend_df,
        x="month",
        y="klausimų skaičius",
        color="komitetas",
        markers=True,
        title="Komitetų klausimų dinamika laikui bėgant",
        labels={"month": "Data", "komitetas": "Komitetas", "klausimų skaičius": "Klausimų skaičius"}
    )

    return html.Div([
        dcc.Graph(figure=fig)
    ], className="card")
