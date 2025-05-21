import pandas as pd
from dash import Dash, dcc, html, Input, Output, State, dash_table
import plotly.express as px

df = pd.read_csv("data/agenda_items_with_topics.csv", encoding="utf-8")

app = Dash(__name__)

app.layout = html.Div([
    html.H2("Seimo komitetų darbotvarkių analizė"),

    html.Div([
        dcc.Dropdown(
            id="committee-dropdown",
            options=[{"label": c, "value": c} for c in sorted(df["committee"].unique())],
            placeholder="Pasirink komitetą",
            multi=True
        ),
        dcc.DatePickerRange(
            id="date-picker",
            min_date_allowed=df["date"].min(),
            max_date_allowed=df["date"].max(),
            start_date=df["date"].min(),
            end_date=df["date"].max(),
        )
    ], style={"display": "flex", "gap": "2rem", "margin-bottom": "1rem"}),

    dcc.Graph(id="topic-bar"),

    dash_table.DataTable(
        id="table",
        columns=[
            {"name": "Data", "id": "date"},
            {"name": "Tema", "id": "topic"},
            {"name": "Klausimas", "id": "question"},
            {"name": "Komitetas", "id": "committee"},
        ],
        page_size=10,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left", "whiteSpace": "normal"},
    )
])


@app.callback(
    Output("table", "data"),
    Output("topic-bar", "figure"),
    Input("committee-dropdown", "value"),
    Input("date-picker", "start_date"),
    Input("date-picker", "end_date")
)
def update_view(committees, start_date, end_date):
    filtered = df.copy()
    if committees:
        filtered = filtered[filtered["committee"].isin(committees)]
    filtered["date"] = pd.to_datetime(filtered["date"])
    filtered = filtered[(filtered["date"] >= start_date) & (filtered["date"] <= end_date)]

    fig = px.histogram(
        filtered,
        x="topic",
        title="Temų pasiskirstymas",
        labels={"topic": "Tema"},
        text_auto=True
    )

    return filtered.to_dict("records"), fig


if __name__ == "__main__":
    app.run(debug=True)
