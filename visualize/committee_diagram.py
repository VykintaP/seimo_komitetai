import pandas as pd
import sqlite3
from dash import html, dcc, Input, Output, callback
import plotly.express as px
from pathlib import Path
from config import DB_PATH, TABLE_CLASSIFIED

DB_PATH = Path(__file__).resolve().parents[1] / "data" / "classified_questions.db"
TABLE_CLASSIFIED = "classified_questions"

def query_df(sql: str) -> pd.DataFrame:
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(sql, conn)
    conn.close()
    return df

def get_committee_chart():
    df = query_df(f"SELECT komitetas FROM {TABLE_CLASSIFIED}")
    df = df[df["komitetas"].notna()]
    committee_counts = df["komitetas"].value_counts().reset_index()
    committee_counts.columns = ["Komitetas", "Klausimų skaičius"]

    fig = px.bar(
        committee_counts,
        x="Klausimų skaičius",
        y="Komitetas",
        orientation="h",
        title="Klausimų skaičius pagal komitetą"
    )

    fig.update_traces(hovertemplate="%{y}: %{x} klausimų")

    return html.Div([
        dcc.Store(id="selected-committee"),
        html.H3("Komitetų pasiskirstymas", style={"color": "#2C3E50"}),
        dcc.Graph(id="committee-bar", figure=fig),
        html.Div(id="theme-by-committee")
    ])

def get_donut_layout(app):
    layout = html.Div([
        get_committee_chart()
    ])

    @app.callback(
        Output("selected-committee", "data"),
        Input("committee-bar", "clickData"),
        prevent_initial_call=True
    )
    def store_selected_committee(clickData):
        if clickData:
            committee = clickData["points"][0]["y"]
            return committee
        return None

    @app.callback(
        Output("theme-by-committee", "children"),
        Input("selected-committee", "data"),
        prevent_initial_call=True
    )
    def update_theme_chart(committee):
        if not committee:
            return html.P("Pasirink komitetą grafike.")

        df = query_df(f"SELECT komitetas, tema FROM {TABLE_CLASSIFIED}")
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

        return html.Div([
            dcc.Graph(figure=fig),
            html.H4(f"Klausimai komitete: {committee}", style={"marginTop": "20px"}),
            dash_table.DataTable(
                columns=[{"name": "Data", "id": "data"}, {"name": "Klausimas", "id": "klausimas"}],
                data=query_df(f"""
                    SELECT data, klausimas FROM {TABLE_CLASSIFIED}
                    WHERE komitetas = '{committee}'
                """).to_dict("records"),
                page_size=15,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"},
            )
        ])

    return layout
