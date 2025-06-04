import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from visualize.utils.topic_labels import TOPIC_LABELS

def get_line_figure(df, selected_topic):
    if df is None or df.empty or "data" not in df.columns or "tema" not in df.columns:
        return go.Figure()

    # Sukuriame stulpelį „metai-mėnuo“
    df["date"] = pd.to_datetime(df["data"], errors="coerce")
    df["month"] = df["date"].dt.to_period("M").astype(str)
    trend = df.groupby(["month", "tema"]).size().reset_index(name="Kiekis")

    # Jei tema pasirinkta, galime ją filtruoti arba spalvinti
    if selected_topic:
        fig = px.line(
            trend,
            x="month",
            y="Kiekis",
            color="tema",
            color_discrete_map={selected_topic: "#C0392B",
                                **{t: "#2C3E50" for t in trend["tema"].unique() if t != selected_topic}}
        )
    else:
        fig = px.line(
            trend,
            x="month",
            y="Kiekis",
            color="tema",
            color_discrete_sequence=["#2C3E50"]
        )

    fig.update_layout(
        xaxis_title="Mėnuo",
        yaxis_title="Klausimų skaičius",
        margin=dict(t=40, b=40, l=60, r=20)
    )
    return fig
