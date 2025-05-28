from dash import Dash, dcc, html
import plotly.express as px
import pandas as pd
from pathlib import Path
from visualize.committee_donut import get_donut_layout
import sqlite3

conn = sqlite3.connect("classified_questions.db")
df = pd.read_sql_query("SELECT * FROM classified_questions", conn)
conn.close()

app = Dash(__name__)
app.title = "Seimo temų analizė"

diagnostics_path = Path(__file__).resolve().parents[1] / "data" / "diagnostics" / "diagnostics.csv"
df = pd.read_csv(diagnostics_path)

fig = px.bar(
    df.sort_values("questions/week", ascending=False),
    x="questions/week",
    y="committee",
    orientation="h",
    labels={"questions/week": "Klausimai per savaitę", "committee": "Komitetas"},
    title="Klausimų per savaitę intensyvumas"
)
fig.update_layout(yaxis=dict(autorange="reversed"))

app.layout = html.Div([
    html.Img(src="/assets/seimas_logo.png", style={"height": "80px", "margin": "20px auto", "display": "block"}),
    html.H1("Seimo komitetų analizė", style={"textAlign": "center"}),
    dcc.Tabs([
        dcc.Tab(label="Intensyvumas", children=[
            html.Div([
                dcc.Graph(figure=fig)
            ], className="card")
        ]),
        dcc.Tab(label="Temų pasiskirstymas", children=[
            get_donut_layout(app)
        ])
    ])
])

if __name__ == "__main__":
    app.run(debug=True)
