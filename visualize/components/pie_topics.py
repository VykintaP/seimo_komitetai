import numpy as np
import pandas as pd
import plotly.graph_objects as go
from dash import dcc

from visualize.utils.topic_labels import TOPIC_LABELS

# Grafikų parametrai ir tekstai
NO_DATA_TITLE = "Temų grafikas – nėra duomenų"
NO_DATA_ANNOTATION = "Nėra duomenų"
DEFAULT_TITLE = "Temų pasiskirstymas – apie ką svarsto Seimo komitetai"
EMPTY_MESSAGE = dict(text=NO_DATA_ANNOTATION, x=0.5, y=0.5, showarrow=False)
PIE_HOLE_RATIO = 0.2
FONT = dict(size=13, color="#36454F")
DEFAULT_COLOR = "#DDDDDD"

# Spalvų paletė grafikams
DARK_PALETTE_EXTENDED = [
    "#000213",
    "#01071B",
    "#020D24",
    "#03132D",
    "#041936",
    "#051E3F",
    "#062448",
    "#082951",
    "#0D3561",
    "#134371",
    "#195181",
    "#1F5F91",
    "#266DA1",
    "#3D7EAB",
    "#548FB5",
    "#6BA0BF",
    "#82B1C9",
    "#99C2D3",
    "#B0D3DD",
]


def shorten(label, limit=30):
    """Sutrumpina ilgą tekstą, įterpdamas naują eilutę kas 30 simbolių"""
    label = str(label) if pd.notnull(label) else ""
    if len(label) <= limit:
        return label
    return "<br>".join([label[i: i + limit] for i in range(0, len(label), limit)])


def filter_dataframe(df: pd.DataFrame, selected_committee: str | list) -> pd.DataFrame:
    """Filtruoja duomenų rinkinį pagal pasirinktą komitetą"""
    if selected_committee:
        if isinstance(selected_committee, list):
            df = df[df["komitetas"].isin(selected_committee)]
        else:
            df = df[df["komitetas"] == selected_committee]
    return df


def generate_no_data_figure() -> go.Figure:
    """Grąžina tuščią grafiką su pranešimu apie duomenų nebuvimą"""
    return go.Figure(layout=dict(title=NO_DATA_TITLE, annotations=[EMPTY_MESSAGE]))


def get_pie_figure(
        df: pd.DataFrame,
        selected_topic: str = None,
        selected_committee: str = None,
        show_all: bool = False,
) -> go.Figure:
    """Generuoja skritulinę diagramą iš duomenų"""
    print("Pasirinkta tema:", selected_topic)
    if df is None or "tema" not in df.columns:
        return generate_no_data_figure()

    df_for_plot = filter_dataframe(df, selected_committee)
    if df_for_plot.empty:
        return generate_no_data_figure()

    # Paruošiam duomenis grafikui
    df_for_plot["tema_lt"] = df_for_plot["tema"].map(TOPIC_LABELS).fillna(df_for_plot["tema"])
    topic_counts = (
        df_for_plot.groupby(["tema", "tema_lt"]).size().reset_index(name="Klausimų skaičius")
    )
    topic_counts = topic_counts.sort_values("Klausimų skaičius", ascending=False)
    top_topics = topic_counts.head(15).copy()

    full_labels = top_topics["tema_lt"].tolist()
    short_labels = ["<br>".join([" ".join(label.split()[i:i+4]) for i in range(0, len(label.split()), 4)]) if isinstance(label, str) else "" for label in full_labels]
    values = top_topics["Klausimų skaičius"].tolist()
    customdata = top_topics["tema"]  # Saugom originalius temų pavadinimus

    total_questions = topic_counts["Klausimų skaičius"].sum()
    top_topics = topic_counts.iloc[:15].copy()
    if len(topic_counts) > 15:
        other_sum = topic_counts.iloc[15:]["Klausimų skaičius"].sum()
        top_topics.loc[len(top_topics)] = {
            "tema": "Kitos temos",
            "tema_lt": "Kitos temos",
            "Klausimų skaičius": other_sum,
        }
    top_topics["Procentas"] = (
            top_topics["Klausimų skaičius"] / total_questions * 100
    ).round(1)

    colors = DARK_PALETTE_EXTENDED[: len(top_topics)]
    highlight_color = "#FF9800"
    colors = []
    for i, topic in enumerate(top_topics["tema"]):
        if selected_topic and topic == selected_topic:
            colors.append(highlight_color)
        else:
            colors.append(DARK_PALETTE_EXTENDED[i % len(DARK_PALETTE_EXTENDED)])

    title = DEFAULT_TITLE
    if selected_topic and selected_topic in df_for_plot["tema"].unique():
        selected_tema_lt = TOPIC_LABELS.get(selected_topic, selected_topic)
        title = f"Temų pasiskirstymas – akcentuota tema: {selected_tema_lt}"

    pulls = [
        0.1 if selected_topic and topic == selected_topic else 0
        for topic in top_topics["tema"]
    ]

    fig = go.Figure(
        go.Pie(
            labels=short_labels,
            values=values,
            customdata=customdata,
            hole=0.5,
            domain=dict(x=[0.2, 0.8], y=[0.2, 0.8]),
            textinfo="label",
            textposition="outside",
            showlegend=False,
            sort=True,
            direction="clockwise",
            rotation=120,
            insidetextorientation="radial",
            textfont=dict(size=14, color="#333"),
            marker=dict(colors=colors, line=dict(color="white", width=2)),
            pull=pulls,
            hovertemplate="<b>%{label}</b><br>Klausimų sk.: %{value} (%{percent})<extra></extra>",
        )
    )

    fig.update_layout(margin=dict(t=10, b=10, l=10, r=10), height=500, showlegend=False)

    return fig