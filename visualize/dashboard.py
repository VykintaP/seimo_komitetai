import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from pathlib import Path

app = Dash(__name__)

def load_summary():
    diagnostics_path = Path(__file__).resolve().parents[1] / "data" / "diagnostics" / "diagnostics.csv"
    df = pd.read_csv(diagnostics_path)
    return df

df = load_summary()

fig = px.bar(
    df.sort_values("questions/week", ascending=False),
    x="questions/week",
    y="committee",
    orientation="h",
    labels={
        "questions/week": "Klausimai per savaitę",
        "committee": "Komitetas (pilnas pavadinimas)"
    },
    title="Klausimų per savaitę intensyvumas"
)

fig.update_layout(yaxis=dict(autorange="reversed"))

app.layout = html.Div([
    html.H2("Komitetų klausimų intensyvumo analizė"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
