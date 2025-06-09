"""Generuoja lentelę su komitetų klausimais pagal pasirinktus filtrus"""
import pandas as pd
from dash import dash_table, html

from visualize.utils.topic_labels import TOPIC_LABELS


def get_questions_table(
        df: pd.DataFrame,
        selected_topic: str = None,
        selected_committee: str = None,
        selected_date: str = None,
):
    if df is None or df.empty:
        return html.Div("Nėra klausimų", className="card")

    df = df.copy()

    # Atrenka klausimus pagal pasirinktą komitetą 
    if selected_committee:
        if isinstance(selected_committee, list):
            df = df[df["komitetas"].isin(selected_committee)]
        else:
            df = df[df["komitetas"] == selected_committee]

    # Atrenka klausimus pagal pasirinktą temą
    if selected_topic:
        df = df[df["tema"] == selected_topic]

    # Atrenka klausimus 3 dienų intervale prieš ir po pasirinktos datos
    if selected_date:
        selected_date_clean = selected_date.strip()
        if selected_date_clean != "RESET":
            try:
                df["data"] = pd.to_datetime(df["data"], errors="coerce")
                selected_dt = pd.to_datetime(selected_date_clean)
                start = selected_dt - pd.Timedelta(days=3)
                end = selected_dt + pd.Timedelta(days=3)
                df = df[(df["data"] >= start) & (df["data"] <= end)]
            except Exception:
                pass

    if df.empty:
        return html.Div("Pasirinkti filtrai nerado klausimų", className="card")

    # Prideda lietuviškus temų pavadinimus
    df["Sritis"] = df["tema"].map(TOPIC_LABELS).fillna(df["tema"])

    # Formatuoja duomenis lentelės atvaizdavimui
    df["data"] = pd.to_datetime(df["data"], errors="coerce").dt.date
    display_columns = ["komitetas", "data", "klausimas", "Sritis"]
    columns = [{"name": name.capitalize(), "id": name} for name in display_columns]
    data = df[display_columns].to_dict("records")

    return html.Div(
        className="dash-table-container",
        children=[
            dash_table.DataTable(
                id="questions-table",
                columns=columns,
                data=data,
                page_action="none",
                fixed_rows={"headers": True},
                style_table={
                    "overflowX": "auto",
                    "overflowY": "auto",
                    "maxHeight": "400px",
                },
                style_cell={
                    "textAlign": "left",
                    "padding": "6px",
                    "fontSize": "13px",
                    "minWidth": "100px",
                    "maxWidth": "300px",
                    "whiteSpace": "normal",
                },
                style_header={
                    "backgroundColor": "#F5F7FA",
                    "fontWeight": "bold",
                    "border": "1px solid #DEE2E6",
                },
                style_data={"border": "1px solid #F0F0F0"},
                style_as_list_view=True,
            )
        ],
    )
