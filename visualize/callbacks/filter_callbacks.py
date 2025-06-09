import copy
import sqlite3

import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, dcc, html, no_update
from utils.db import query_df
from utils.filtering import filter_df_by_filters

from config import TABLE_CLASSIFIED
from visualize.utils.topic_labels import TOPIC_LABELS

# Pranešimas apie modulio įkėlimą
print("[CALLBACKS] filter_callbacks.py įkeltas")

import logging
import os
import sqlite3


# Grąžina unikalių komitetų sąrašą iš duomenų bazės
def fetch_distinct_committees():
    project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    absolute_db_path = os.path.join(project_root, "data", "classified_questions.db")

    if not os.path.exists(absolute_db_path):
        raise FileNotFoundError(f"Database file not found at: {absolute_db_path}")

    with sqlite3.connect(absolute_db_path) as connection:
        cursor = connection.cursor()
        cursor.execute("SELECT DISTINCT komitetas FROM classified_questions")
        return [row[0] for row in cursor.fetchall()]


# Inicializuojam komitetų sąrašą 
try:
    committee_list = fetch_distinct_committees()
    print("Komitetų sąrašas:", committee_list)
except Exception as e:
    print(f"Klaida gaunant komitetus: {e}")
    committee_list = []

committee_map = {i: name for i, name in enumerate(committee_list)}


@callback(
    Output("filtered-df", "data"),
    Input("date-picker-range", "start_date"),
    Input("date-picker-range", "end_date"),
    Input("selected-committee", "data"),
    Input("selected-topic", "data"),
    Input("selected-date", "data"),
)
def update_filtered_df(
        start_date, end_date, selected_committee, selected_topic, selected_date
):
    import re

    df = query_df(f"SELECT * FROM {TABLE_CLASSIFIED}")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    logging.debug("[filtered-df] Pradinis įrašų kiekis: %d", len(df))

    # Nustatome datų filtrą - aplink pasirinktą datą arba pagal intervalą
    date_for_filtering = None
    if (
            selected_date
            and isinstance(selected_date, str)
            and selected_date.strip()
            and selected_date.strip() != "RESET"
    ):
        # Gali būti su UUID (pvz. 2025-06-01__x4fs)
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", selected_date.strip())
        if date_match:
            date_for_filtering = pd.to_datetime(date_match.group(1)).normalize()
            start = date_for_filtering - pd.Timedelta(days=3)
            end = date_for_filtering + pd.Timedelta(days=3)
        else:
            logging.warning(
                "[filtered-df] Nepavyko išskirti datos iš selected-date: %s",
                selected_date,
            )
            start = pd.to_datetime(start_date) if start_date else None
            end = pd.to_datetime(end_date) if end_date else None
    else:
        start = pd.to_datetime(start_date) if start_date else None
        end = pd.to_datetime(end_date) if end_date else None

    # Paruošiam filtrus duomenų atrinkimui
    filters = {
        "start": start,
        "end": end,
        "committees": [selected_committee] if selected_committee else [],
        "topics": [selected_topic] if selected_topic else [],
    }

    df_filtered = filter_df_by_filters(df, filters)
    logging.debug("[filtered-df] Po filtravimo liko: %d įrašų", len(df_filtered))

    return copy.deepcopy(df_filtered.to_dict("records"))


@callback(
    Output("other-topics-detail", "children"),
    Input("pie-topics", "clickData"),
    State("filtered-df", "data"),
    prevent_initial_call=True,
)
def show_other_topics_detail(clickData, data):
    if not clickData or not data:
        return html.Div()

    selected = clickData["points"][0]["label"].split(" (")[0]
    if selected != "Kitos temos":
        return html.Div()

    df = pd.DataFrame(data)
    df["tema_lt"] = df["tema"].map(TOPIC_LABELS).fillna(df["tema"])

    counts = df["tema_lt"].value_counts()
    top_6 = counts.head(6).index
    others = df[df["tema_lt"].isin(counts.index.difference(top_6))]

    if others.empty:
        return html.Div("Nėra papildomų temų.")

    theme_counts = others["tema_lt"].value_counts().reset_index()
    theme_counts.columns = ["Tema", "Klausimų sk."]

    # Formuojam skritulinę diagramą kitoms temoms
    fig = go.Figure(
        go.Pie(
            labels=theme_counts["Tema"],
            values=theme_counts["Klausimų sk."],
            hole=0.5,
            textinfo="label+percent",
            textposition="outside",
            marker=dict(line=dict(color="white", width=1.5)),
            hovertemplate="<b>%{label}</b><br>Klausimų sk.: %{value}<br>%{percent}<extra></extra>",
        )
    )

    fig.update_layout(
        height=360,
        margin=dict(t=30, b=20, l=20, r=20),
        title="„Kitos temos"
    )

    return html.Div(
        [
            html.H4("Kitos temos detalizuotos:"),
            dcc.Graph(figure=fig, config={"displayModeBar": False}),
        ]
    )


@callback(
    Output("date-filter", "start_date"),
    Output("date-filter", "end_date"),
    Input("reset-date", "n_clicks"),
    prevent_initial_call=True,
)
def reset_date_range(n_clicks):
    # Atstatom datos filtrus į pradinę būseną
    df = query_df(f"SELECT * FROM {TABLE_CLASSIFIED}")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df["data"].min().date(), df["data"].max().date()


@callback(
    Output("filtered-bar-data", "data"),
    Input("raw-data", "data"),
    Input("selected-topic", "data"),
    Input("selected-date", "data"),
)
def filter_bar_chart_data(raw_data, selected_topic, selected_date):
    import re

    df = pd.DataFrame(raw_data)
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Filtruojam pagal temą
    if selected_topic:
        df = df[df["tema"] == selected_topic]

    # Filtruojam pagal datą (+-3 dienos)
    if (
            selected_date
            and isinstance(selected_date, str)
            and selected_date.strip() != "RESET"
    ):
        date_match = re.match(r"(\d{4}-\d{2}-\d{2})", selected_date.strip())
        if date_match:
            selected_dt = pd.to_datetime(date_match.group(1))
            start = selected_dt - pd.Timedelta(days=3)
            end = selected_dt + pd.Timedelta(days=3)
            df = df[(df["data"] >= start) & (df["data"] <= end)]
    else:
        df = df.copy()  # Perkrauname visus duomenis

    return df.to_dict("records")
