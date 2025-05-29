import pandas as pd
import sqlite3
from dash import html, dcc, Input, Output, callback
import plotly.express as px
from pathlib import Path

db_path = Path(__file__).resolve().parents[1] / "data" / "classified_questions.db"

def get_committee_donut():
    conn = sqlite3.connect(db_path)
    df = pd.read_sql_query("SELECT komitetas FROM classified_questions", conn)
    conn.close()

    df = df[df["komitetas"].notna()]
    committee_counts = df["komitetas"].value_counts().reset_index()
    committee_counts.columns = ["Komitetas", "Klausimų skaičius"]

    fig = px.pie(
        committee_counts,
        names="Komitetas",
        values="Klausimų skaičius",
        hole=0.5,
        title="Klausimų skaičius pagal komitetą"
    )

    fig.update_traces(textposition="inside", textinfo="percent+label", hoverinfo="label+value")

    return html.Div([
        dcc.Store(id="selected-committee"),
        html.H3("Komitetų pasiskirstymas", style={"color": "#2C3E50"}),
        dcc.Graph(id="committee-donut", figure=fig),
        html.Div(id="theme-by-committee")
    ])


def get_donut_layout(app):
    layout = html.Div([
        get_committee_donut()
    ])

    @app.callback(
        Output("selected-committee", "data"),
        Input("committee-donut", "clickData"),
        prevent_initial_call=True
    )
    def store_selected_committee(clickData):
        if clickData:
            committee = clickData["points"][0]["label"]
            return committee
        return None

    @app.callback(
        Output("theme-by-committee", "children"),
        Input("selected-committee", "data"),
        prevent_initial_call=True
    )
    def update_theme_chart(committee):
        if not committee:
            return html.P("Pasirink komitetą donut grafike.")

        conn = sqlite3.connect(db_path)
        df = pd.read_sql_query("SELECT komitetas, tema FROM classified_questions", conn)
        conn.close()

        df = df[(df["komitetas"] == committee) & (df["tema"].notna())]
        theme_counts = df["tema"].value_counts().reset_index()
        theme_counts.columns = ["Tema", "Klausimų skaičius"]

        fig = px.bar(
            theme_counts,
            x="Klausimų skaičius",
            y="Tema",
            orientation="h",
            title=f"Temos komitete: {committee}"
        )

        fig.update_traces(hovertemplate="%{y}: %{x} klausimų")

        return dcc.Graph(figure=fig)

    return layout
