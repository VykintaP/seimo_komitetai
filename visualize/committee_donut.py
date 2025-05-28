import pandas as pd
import plotly.express as px
from dash import html, dcc, Input, Output
from pathlib import Path

def get_donut_layout(app):
    classified_dir = Path(__file__).resolve().parents[1] / "data" / "classified"
    files = list(classified_dir.glob("*.csv"))

    committees = {
        file.name: file.stem.replace("_", " ").title()
        for file in files
        if "theme" in pd.read_csv(file).columns
    }

    seimas_colors = ['#AE1C28', '#FDB913', '#007A33', '#000000', '#555555', '#999999', '#CCCCCC']

    layout = html.Div([
        html.H2("Temų pasiskirstymas pagal pasirinktą komitetą"),
        html.Div([
            dcc.Dropdown(
                id="committee-dropdown",
                options=[{"label": v, "value": k} for k, v in committees.items()],
                value=list(committees.keys())[0],
                className="dash-dropdown"
            )
        ], className="card"),

        html.Div([
            dcc.Graph(id="donut-chart"),
            html.Div(id="summary-text", style={
                "textAlign": "center",
                "fontSize": "16px",
                "color": "#2C3E50",
                "marginTop": "10px"
            })
        ], className="card")
    ])

    @app.callback(
        [Output("donut-chart", "figure"),
         Output("summary-text", "children")],
        Input("committee-dropdown", "value")
    )
    def update_donut_chart(selected_file):
        path = classified_dir / selected_file
        df = pd.read_csv(path)
        df = df[df["theme"].notna()]

        counts = df.groupby("theme").agg({
            "question": "first",
            "theme": "count"
        }).rename(columns={
            "theme": "Klausimų skaičius",
            "question": "Pavyzdinis klausimas"
        }).reset_index()
        counts = counts.rename(columns={"theme": "Tema"})

        # Trumpesnė tema legendoje
        counts["Trumpas pavadinimas"] = counts["Tema"].apply(lambda x: x.split(",")[0])

        fig = px.pie(
            counts,
            names="Trumpas pavadinimas",
            values="Klausimų skaičius",
            hole=0.4,
            title=committees[selected_file],
            hover_data=["Tema", "Pavyzdinis klausimas"],
            color_discrete_sequence=seimas_colors
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")
        fig.update_layout(margin={"t": 60, "b": 20, "l": 20, "r": 20})

        return fig, f"Iš viso nagrinėta {df.shape[0]} klausimų."

    return layout
