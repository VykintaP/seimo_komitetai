import plotly.express as px

def get_committees_bar(df):
    counts = df["komitetas"].value_counts().reset_index()
    counts.columns = ["Komitetas", "Kiekis"]
    counts = counts.sort_values("Kiekis", ascending=True)

    fig = px.bar(
        counts,
        x="Kiekis",
        y="Komitetas",
        orientation="h",
        text="Kiekis",
        color_discrete_sequence=["#2C3E50"]
    )

    fig.update_traces(textposition="outside")
    fig.update_layout(
        height=500,
        margin=dict(l=180, r=20, t=40, b=40),
        xaxis_title="Klausimų skaičius",
        yaxis_title=None,
        showlegend=False
    )

    return fig
