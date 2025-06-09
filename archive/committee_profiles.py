from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
from dash import dcc, html

root = Path(__file__).resolve().parents[1]
diagnostics_path = root / "data" / "diagnostics" / "diagnostics.csv"
diagnostics_df = pd.read_csv(diagnostics_path)


def create_committee_card(committee_data):
    return html.Div(
        [
            html.H4(committee_data["committee"]),
            html.Div(
                [
                    dcc.Graph(
                        figure=go.Figure(
                            go.Indicator(
                                mode="number",
                                value=committee_data["questions/week"],
                                title={"text": "Kiek klausimų per savaitę?"},
                                number={"suffix": ""},
                            )
                        )
                    ),
                    dcc.Graph(
                        figure=go.Figure(
                            go.Indicator(
                                mode="number",
                                value=committee_data["unique_dates"],
                                title={"text": "Unikalios datos"},
                            )
                        )
                    ),
                    dcc.Graph(
                        figure=go.Figure(
                            go.Indicator(
                                mode="number",
                                value=committee_data["avg_q_per_date"],
                                title={"text": "Vid. klausimų / posėdį"},
                            )
                        )
                    ),
                    dcc.Graph(
                        figure=go.Figure(
                            go.Indicator(
                                mode="number",
                                value=committee_data["questions"],
                                title={"text": "Viso klausimų"},
                            )
                        )
                    ),
                ],
                style={
                    "display": "grid",
                    "gridTemplateColumns": "repeat(2, 1fr)",
                    "gap": "10px",
                },
            ),
        ],
        style={
            "backgroundColor": "#F5F7FA",
            "padding": "1rem",
            "borderRadius": "1rem",
            "boxShadow": "0 4px 6px rgba(0, 0, 0, 0.1)",
            "marginBottom": "2rem",
        },
    )


def get_committee_profiles_layout():
    committee_cards = [
        create_committee_card(row) for _, row in diagnostics_df.iterrows()
    ]
    return html.Div(
        [html.H2("Komitetų profiliai", style={"color": "#2C3E50"}), *committee_cards]
    )
