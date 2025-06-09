import pandas as pd
import plotly.express as px
import plotly.graph_objects as go


def get_donut_figure(
    df: pd.DataFrame, selected_topic=None, selected_committee=None, show_all=False
):
    """
    Sukuria donnut diagramą
    """
    if df.empty or "tema" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Temų donut diagrama – nėra duomenų")
        return fig

    if selected_committee and selected_committee in df["komitetas"].unique():
        df = df[df["komitetas"] == selected_committee]

    topic_counts = df["tema"].value_counts().reset_index()
    topic_counts.columns = ["Tema", "Klausimų skaičius"]

    if not show_all and len(topic_counts) > 8:
        other_count = topic_counts.iloc[8:]["Klausimų skaičius"].sum()
        main_topics = topic_counts.iloc[:8].copy()
        other_row = pd.DataFrame(
            {"Tema": ["Kitos temos"], "Klausimų skaičius": [other_count]}
        )
        topic_counts = pd.concat([main_topics, other_row], ignore_index=True)

    fig = px.pie(
        topic_counts,
        values="Klausimų skaičius",
        names="Tema",
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Set2,
    )

    if selected_topic:
        fig.update_traces(
            marker=dict(
                colors=[
                    "#C0392B" if name == selected_topic else "#2C3E50"
                    for name in topic_counts["Tema"]
                ]
            )
        )

    fig.update_traces(
        textposition="inside",
        textinfo="percent+label",
        insidetextfont=dict(color="white"),
        hoverinfo="label+percent+value",
        marker=dict(line=dict(color="#FFFFFF", width=2)),
    )

    fig.update_layout(
        margin=dict(t=30, b=0, l=20, r=20),
        legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
        plot_bgcolor="#FFFFFF",
        paper_bgcolor="#FFFFFF",
    )

    return fig
