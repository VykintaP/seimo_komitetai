import logging

import pandas as pd
import plotly.graph_objects as go
from dash import dcc

# Paletė iš tamsiai mėlynų į šviesiai žalius atspalvius
BAR_CHART_PALETTE = [
    "#003B2E",
    "#004C3B",
    "#0A5C44",
    "#1F6C52",
    "#2E7D59",
    "#3D8F61",
    "#4EA268",
    "#5DB471",
    "#6DC77B",
    "#7FC78A",
    "#90D39A",
    "#9ADBA1",
    "#A7E1AD",
    "#B6EEC0",
    "#C3F2CD",
    "#D0F5D8",
    "#DDF8E3",
    "#E9FBEF",
    "#F2FCF5",
    "#FAFEFB",
]

logging.basicConfig(level=logging.DEBUG)


def get_committees_bar(df: pd.DataFrame, selected_committee: str = None) -> go.Figure:
    """Generuoja horizontalią stulpelinę diagramą rodančią komitetų klausimų statistiką"""
    logging.debug(f"[DEBUG] Gauta {len(df)} eilučių BarChart'ui (po filtravimo)")

    if df.empty or "komitetas" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Komitetų grafikas – nėra duomenų")
        return fig

    # Pašalina žodį "komitetas" ir tarpus iš pavadinimo
    df["komitetas_clean"] = (
        df["komitetas"]
        .str.replace(r"\bkomitetas\b[:\s–-]*", "", case=False, regex=True)
        .str.strip()
    )

    # Sudaro visų komitetų sąrašą
    all_committees = df["komitetas_clean"].dropna().unique()
    base_counts = pd.DataFrame({"Komitetas": all_committees})

    # Skaičiuoja kiekvieno komiteto klausimų kiekį
    counts_filtered = df["komitetas_clean"].value_counts().reset_index()
    counts_filtered.columns = ["Komitetas", "Klausimų skaičius"]

    # Apjungia duomenis ir užpildo trūkstamus nulinėmis reikšmėmis
    counts = base_counts.merge(counts_filtered, on="Komitetas", how="left").fillna(0)
    counts["Klausimų skaičius"] = counts["Klausimų skaičius"].astype(int)
    counts = counts.sort_values("Klausimų skaičius", ascending=False).head(16)

    # Paruošia pasirinkto komiteto pavadinimą palyginimui
    selected_committee_cleaned = (
        selected_committee.replace(" komitetas", "").strip()
        if selected_committee
        else None
    )

    # Nustato stulpelių spalvas ir linijų storį
    colors = []
    line_widths = []

    for komitetas in counts["Komitetas"]:
        if selected_committee_cleaned and komitetas == selected_committee_cleaned:
            colors.append("#FFA500")  # Oranžinė spalva pažymi pasirinktą komitetą
            line_widths.append(3)
        else:
            colors.append(BAR_CHART_PALETTE[len(colors)])
            line_widths.append(1)

    # Formuoja stulpelinę diagramą
    fig = go.Figure(
        go.Bar(
            x=counts["Klausimų skaičius"],
            y=counts["Komitetas"],
            orientation="h",
            marker=dict(color=colors, line=dict(color="black", width=line_widths)),
            hovertemplate="<b>%{y}</b><br>Klausimų sk.: %{x}<extra></extra>",
            text=counts["Klausimų skaičius"],
            textposition="outside",
        )
    )

    # Nustato diagramos parametrus
    fig.update_layout(
        title=None,
        margin=dict(t=30, b=40, l=30, r=30),
        height=500,
        xaxis=dict(
            title=None,
            tickfont=dict(size=12),
            tickangle=0,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=13),
            automargin=True,
            categoryorder="total ascending",
        ),
        plot_bgcolor="#FAFAFA",
    )
    return fig


def get_committees_bar_chart(df: pd.DataFrame, selected_committee: str = None):
    """Suformuoja Dash komponentą su komitetų stulpeline diagrama"""
    fig = get_committees_bar(df, selected_committee)
    return dcc.Graph(figure=fig, id="bar-committees", config={"displayModeBar": False})
