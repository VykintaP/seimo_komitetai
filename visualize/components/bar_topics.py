import plotly.express as px
import plotly.graph_objects as go
from visualize.utils.topic_labels import TOPIC_LABELS

def get_bar_figure(df, selected_topic=None):
    print(f"[DEBUG] bar_figure: rows={len(df)}")

    if df is None or df.empty or "tema" not in df.columns:
        return go.Figure()
    df["tema_lt"] = df["tema"].map(TOPIC_LABELS).fillna(df["tema"])
    topic_counts = df["tema_lt"].value_counts().reset_index()
    topic_counts.columns = ["tema", "kiekis"]

    fig = px.bar(
        topic_counts,
        x="kiekis",
        y="tema",
        orientation="h",
        color="tema",
        color_discrete_sequence=["#2C3E50"] * len(topic_counts)
    )

    # Jei yra pasirinkta tema – pažymim kita spalva
    if selected_topic and selected_topic in topic_counts["tema"].values:
        colors = ["#C0392B" if t == selected_topic else "#2C3E50" for t in topic_counts["tema"]]
        fig.update_traces(marker_color=colors)

    fig.update_layout(
        yaxis_title="",
        xaxis_title="Klausimų skaičius",
        yaxis=dict(automargin=True),
        margin=dict(t=40, b=40, r=20),
        showlegend = False

    )

    return fig

