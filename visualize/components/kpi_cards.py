import pandas as pd
from dash import html
from visualize.utils.topic_labels import TOPIC_LABELS

"""Generuoja KPI korteles su pagrindiniais rodikliais"""

def generate_kpi_cards(filtered_df: pd.DataFrame):
    # Jei nėra duomenų, grąžiname tuščią būseną
    if filtered_df.empty:
        return html.Div("Nėra duomenų", className="kpi-empty")

    # Išrenkame populiariausią temą ir komitetą
    top_topic_raw = filtered_df["tema"].value_counts().idxmax()
    top_topic = TOPIC_LABELS.get(top_topic_raw, top_topic_raw)
    top_committee = filtered_df["komitetas"].value_counts().idxmax()

    # Skaičiuojame vidutinį klausimų kiekį per savaitę
    filtered_df["data"] = pd.to_datetime(filtered_df["data"])
    weeks = (filtered_df["data"].max() - filtered_df["data"].min()).days / 7
    avg_per_week = round(len(filtered_df) / weeks, 1) if weeks else len(filtered_df)

    return html.Div(
        [
            html.Div([html.H4("Top tema"), html.P(top_topic)], className="kpi-box"),
            html.Div(
                [html.H4("Aktyviausias komitetas"), html.P(top_committee)],
                className="kpi-box",
            ),
            html.Div(
                [
                    html.H4("Vid. klausimų per savaitę"),
                    html.P(f"{avg_per_week} / sav."),
                ],
                className="kpi-box",
            ),
        ],
        className="kpi-zone",
    )
