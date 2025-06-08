from dash import html, dcc
import pandas as pd
from visualize.utils.db import query_df
from config import TABLE_CLASSIFIED


def get_filters():

    committee_options = get_committee_options()

    return html.Div(className="grid-filters", children=[
        dcc.Dropdown(
            id="committee-filter",
            options=committee_options,
            placeholder="Pasirink komitetą (-us)",
            multi=True,
            clearable=True
        ),
        dcc.DatePickerRange(
            id="date-filter",
            display_format="YYYY-MM-DD",
            start_date_placeholder_text="Data nuo",
            end_date_placeholder_text="Data iki",
            minimum_nights=0
        )
    ])


def get_committee_options() -> list[dict]:

    try:
        df = query_df(f"SELECT DISTINCT komitetas FROM {TABLE_CLASSIFIED} ORDER BY komitetas")
        komitetai = df["komitetas"].dropna().unique()
        return [{"label": kom, "value": kom} for kom in komitetai]
    except Exception as e:
        print("[ERROR] Nepavyko gauti komitetų iš DB:", e)
        return []


def filter_df_by_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:

    # Data formatavimas
    if not pd.api.types.is_datetime64_any_dtype(df["data"]):
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    start = filters.get("start")
    end = filters.get("end")

    if start and end:
        start = pd.to_datetime(start)
        end = pd.to_datetime(end)
        df = df[(df["data"] >= start) & (df["data"] <= end)]

    committees = filters.get("committees")
    if committees:
        df = df[df["komitetas"].isin(committees)]

    return df
