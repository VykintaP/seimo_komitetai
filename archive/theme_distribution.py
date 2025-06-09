import sqlite3
from pathlib import Path

import pandas as pd
import plotly.express as px
from dash import Input, Output, State, callback, dash_table, dcc, html

from config import DB_PATH, TABLE_CLASSIFIED

conn = sqlite3.connect(DB_PATH)
schema = pd.read_sql_query(f"PRAGMA table_info({TABLE_CLASSIFIED})", conn)
conn.close()


def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(
        "SELECT data, klausimas, tema FROM classified_questions", conn
    )
    conn.close()
    df = df[df["tema"].notna()]
    return df


df_all = load_data()


def get_theme_distribution_layout():
    db_path = Path(__file__).resolve().parents[1] / "data" / "classified_questions.db"
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT tema FROM classified_questions", conn)
    conn.close()

    df = df[df["tema"].notna()]
    theme_counts = df["tema"].value_counts().reset_index()
    theme_counts.columns = ["Tema", "Klausimų skaičius"]

    fig = px.bar(
        theme_counts,
        x="Klausimų skaičius",
        y="Tema",
        orientation="h",
        title="Temų pasiskirstymas",
        labels={"Tema": "Tema", "Klausimų skaičius": "Klausimų skaičius"},
    )

    fig.update_traces(
        hovertemplate="%{y}: %{x} klausimų<br>(spausk norėdamas peržiūrėti)"
    )

    return html.Div(
        [
            dcc.Store(id="selected-theme"),
            dcc.Tabs(
                id="main-tabs",
                value="distribution",
                children=[
                    dcc.Tab(
                        label="Temų pasiskirstymas",
                        value="distribution",
                        children=[dcc.Graph(id="theme-bar", figure=fig)],
                    ),
                    dcc.Tab(
                        label="Klausimai pagal pasirinktą temą",
                        value="questions",
                        children=[html.Div(id="questions-container")],
                    ),
                ],
            ),
        ]
    )
