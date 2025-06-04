from dash import dcc, html
from visualize.utils.db import query_df
import pandas as pd
from config import TABLE_CLASSIFIED
from visualize.components.filters import get_filters

def get_initial_data():
    df = query_df(f"SELECT * FROM {TABLE_CLASSIFIED}")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    return df.to_dict("records")


def serve_layout():
    return html.Div(className="main-container", children=[
        dcc.Store(id="filtered-df"),
        dcc.Store(id="selected-topic"),
        dcc.Store(id="committee-filter"),
        html.H1("Ką veikia Seimo komitetai?"),

        get_filters(),

        dcc.Tabs(id="main-tabs", value="dashboard", children=[
            dcc.Tab(label="Posėdžių radaras", value="dashboard", className="tab", selected_className="tab--selected"),
            dcc.Tab(label="Apie projektą", value="info", className="tab", selected_className="tab--selected")
        ]),
        html.Div(id="tab-content")
    ])
