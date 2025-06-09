import pandas as pd
from dash import dcc, html

from config import TABLE_CLASSIFIED
from visualize.utils.db import query_df


def get_initial_data() -> list[dict]:
    """Gauna pradinius duomenis iš DB ir paruošia juos naudojimui"""
    df = query_df(f"SELECT * FROM {TABLE_CLASSIFIED}")
    print(df.head())
    df["data"] = pd.to_datetime(df["data"], errors="coerce")
    print("Converted dates:")
    print(df["data"].head())
    return df.to_dict("records")


def serve_layout() -> html.Div:
    """Sugeneruoja pagrindinį puslapio išdėstymą su filtrais ir turiniu"""
    df = query_df(f"SELECT * FROM {TABLE_CLASSIFIED}")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")

    return html.Div(
        className="main-container",
        children=[
            dcc.Store(id="selected-topic"),
            dcc.Store(id="filtered-df", data=get_initial_data()),
            dcc.Store(id="selected-committee"),
            dcc.Store(id="selected-date"),
            dcc.Store(id="raw-data", data=get_initial_data()),
            dcc.Store(id="filtered-bar-data"),
            # Puslapio antraštė ir aprašymas 
            html.Div(
                [
                    html.H1("Seimo komitetų radaras", className="dashboard-title"),
                    html.P(
                        "Temos, skaičiai ir sprendimai – Seimo komitetų veikla skaidriai",
                        className="subtitle",
                    ),
                    html.Div(
                        [
                            dcc.Link(
                                "Daugiau apie projektą",
                                href="/info",
                                className="about-link",
                            )
                        ],
                        className="about-container",
                    ),
                ],
                className="dashboard-header",
            ),
            html.Div(
                className="active-filters-bar",
                children=[html.Div(id="active-filters", className="active-filters")],
            ),
            # Datos intervalo pasirinkimas
            html.Div(
                className="filter-controls top-filters",
                children=[
                    html.Div(
                        children=[
                            dcc.DatePickerRange(
                                id="date-picker-range",
                                start_date=df["data"].min().date(),
                                end_date=df["data"].max().date(),
                                min_date_allowed=df["data"].min().date(),
                                max_date_allowed=df["data"].max().date(),
                                initial_visible_month=df["data"].max().date(),
                                display_format="YYYY-MM-DD",
                                className="date-picker-range",
                            ),
                            html.Button(
                                "Išvalyti filtrus",
                                id="clear-filters-btn",
                                className="reset-button",
                                n_clicks=0,
                            ),
                        ],
                        className="date-filter-row",
                    )
                    # Alternatyvi filtro išvalymo mygtukas
                    # html.Button(
                    #     "Išvalyti filtrus",
                    #     id="reset-filters-btn",
                    #     className="filter-clear-button",
                    #     n_clicks=0
                    # )
                ],
            ),
            html.Div(id="dashboard-content", className="dashboard-content"),
        ],
    )
