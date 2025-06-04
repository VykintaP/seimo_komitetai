from dash import html, dcc
import plotly.express as px
from visualize.utils.db import query_df
from config import TABLE_CLASSIFIED

def get_committee_chart():
    df = query_df(f"SELECT komitetas FROM {TABLE_CLASSIFIED}")
    df = df[df["komitetas"].notna()]
    committee_counts = df["komitetas"].value_counts().reset_index()
    committee_counts.columns = ["Komitetas", "Klausimų skaičius"]

    fig = px.bar(
        committee_counts,
        x="Klausimų skaičius",
        y="Komitetas",
        orientation="h",
        title="Klausimų skaičius pagal komitetą"
    )
    fig.update_traces(hovertemplate="%{y}: %{x} klausimų")

    return html.Div([
        dcc.Store(id="selected-committee"),
        html.H3("Komitetų pasiskirstymas", style={"color": "#2C3E50"}),
        dcc.Graph(id="committee-bar", figure=fig),
        html.Div(id="theme-by-committee")
    ])



