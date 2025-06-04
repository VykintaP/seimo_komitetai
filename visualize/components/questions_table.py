import pandas as pd
from dash import dash_table, html
from visualize.utils.topic_labels import TOPIC_LABELS

def get_questions_table(df, selected_topic):
    if df is None or df.empty:
        return html.Div("Nėra klausimų", className="card")

    if selected_topic:
        df = df[df["tema"] == selected_topic]
    # Stulpeliai, kuriuos rodysime
    columns = [
        {"name": "Komitetas", "id": "komitetas"},
        {"name": "Data", "id": "data"},
        {"name": "Klausimas", "id": "klausimas"},
        {"name": "Tema", "id": "tema"},
        {"name": "Projektas", "id": "projektas"},
        {"name": "Atsakingi", "id": "atsakingi"},
        {"name": "Dalyviai", "id": "dalyviai"},
    ]
    data = df.to_dict("records")
    return html.Div(className="dash-table-container", children=[
        html.H3("Klausimų sąrašas"),
        dash_table.DataTable(
            id="questions-table",
            columns=columns,
            data=data,
            page_size=10,
            style_cell={"textAlign": "left", "padding": "5px"},
            style_header={"backgroundColor": "#F5F7FA", "fontWeight": "bold"}
        )
    ])
