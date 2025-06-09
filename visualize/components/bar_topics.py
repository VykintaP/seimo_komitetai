# visualize/components/bar_topics.py

import pandas as pd
import plotly.graph_objects as go

from visualize.utils.topic_labels import TOPIC_LABELS


def get_bar_figure(df: pd.DataFrame, selected_topic: str = None) -> go.Figure:
    """Grąžina horizontalią juostinę diagramą su temų dažnumu bei paryškina pasirinktą temą"""
    print(f"[DEBUG] bar_figure: rows={len(df)}")

    if df is None or df.empty or "tema" not in df.columns:
        return go.Figure()

    # Konvertuoja temų pavadinimus į lietuvių kalbą
    df["tema_lt"] = df["tema"].map(TOPIC_LABELS).fillna(df["tema"])
    topic_counts = df["tema_lt"].value_counts(sort=False).reset_index()
    topic_counts.columns = ["tema", "kiekis"]

    # Pasirinktai temai naudoja raudoną spalvą, kitoms - mėlyną
    colors = [
        "#C0392B" if t == selected_topic else "#2C3E50" for t in topic_counts["tema"]
    ]

    # Sukuria horizontalią juostinę diagramą
    fig = go.Figure(
        go.Bar(
            x=topic_counts["kiekis"],
            y=topic_counts["tema"],
            orientation="h",
            marker_color=colors,
        )
    )

    # Nustato diagramos parametrus
    fig.update_layout(
        title="Temų dažnumas",
        xaxis_title="Klausimų skaičius",
        yaxis=dict(title="", automargin=True),
        margin=dict(t=40, b=40, r=20),
        showlegend=False,
    )

    return fig
