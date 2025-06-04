import plotly.express as px
import plotly.graph_objects as go
from visualize.utils.topic_labels import TOPIC_LABELS

def get_pie_figure(df, selected_topic):
    if df is None or df.empty or "tema" not in df.columns:
        return go.Figure()


    df["tema_lt"] = df["tema"].map(TOPIC_LABELS).fillna(df["tema"])
    counts = df["tema_lt"].value_counts(normalize=True).reset_index()
    counts.columns = ["Tema", "Procentas"]
    counts["Procentas"] = (counts["Procentas"] * 100).round(1)

    fig = px.pie(
        counts,
        values="Procentas",
        names="Tema",
        hole=0.5,
        color_discrete_sequence=["#2C3E50", "#C0392B", "#F4D03F", "#95A5A6"]
    )

    if selected_topic and selected_topic in counts["Tema"].values:
        fig.update_traces(
            pull=[0.1 if t == selected_topic else 0 for t in counts["Tema"]],
            marker=dict(line=dict(color="#FFFFFF", width=2))
        )

    # Tooltip formatavimas – aiškus procentas
    fig.update_traces(
        hole=0.5,  # didesnė skylė – mažiau vizualinio svorio
        textposition="outside",
        textinfo="percent+label",
        hovertemplate="%{label}: %{value}%"
    )

    # Layout: legenda apačioje, šriftas, automatinis teksto valdymas
    total_questions = int(df.shape[0])

    fig.update_layout(
        height=500,
        margin=dict(t=60, b=60, l=40, r=180),
        legend=dict(
            orientation="v",
            yanchor="middle",
            y=0.5,
            xanchor="left",
            x=1.1,
            title=None,
            font=dict(size=11)
        ),
        uniformtext_minsize=12,
        uniformtext_mode="hide",
        annotations=[dict(
            text=f"{total_questions} klaus.",
            x=0.5, y=0.5,
            font_size=20,
            showarrow=False
        )]
    )

    return fig
