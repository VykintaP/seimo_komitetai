from dash import html, dcc
from visualize.utils.db import query_df
from config import TABLE_CLASSIFIED
import pandas as pd


def get_filters():
    df = query_df(f"SELECT DISTINCT komitetas FROM {TABLE_CLASSIFIED}")
    committees = sorted(df["komitetas"].dropna().unique())

    return html.Div(className="grid-filters", children=[

        dcc.DatePickerRange(
            id="date-filter",
            display_format="YYYY-MM-DD",
            start_date_placeholder_text="Data nuo",
            end_date_placeholder_text="Data iki",
            minimum_nights=0
        )
    ])

def get_committee_options():
    df = query_df("SELECT DISTINCT komitetas FROM classified_questions ORDER BY komitetas")
    return [{"label": k, "value": k} for k in df["komitetas"].dropna().unique()]

def filter_df_by_filters(df, filters: dict) -> pd.DataFrame:
    if "start" in filters and "end" in filters:
        df = df[(df["data"] >= filters["start"]) & (df["data"] <= filters["end"])]

    committees = filters.get("committees")
    if committees:  # tik jei pasirinkta bent viena reikšmė
        df = df[df["komitetas"].isin(committees)]

    return df
