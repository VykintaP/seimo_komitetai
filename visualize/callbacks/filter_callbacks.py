from dash import Input, Output, callback
import pandas as pd
from datetime import date
from utils.db import query_df
from utils.filtering import filter_df_by_filters
from config import TABLE_CLASSIFIED  # jei turi
import pandas as pd


@callback(
    Output("filtered-df", "data"),
    Input("committee-filter", "value"),
    Input("date-filter", "start_date"),
    Input("date-filter", "end_date")
)
def update_filtered_df(committees, start, end):
    print("[DEBUG] Filter input:", committees, start, end)

    df = query_df(f"SELECT * FROM {TABLE_CLASSIFIED}")  # ar bent jau tiesioginis "classified_questions"
    print("[DEBUG] Before filtering:", df.shape)
    print(df.head(3).to_string(index=False))

    filters = {
        "committees": committees or [],
        "start": start or "2020-01-01",
        "end": end or "2025-12-31"
    }
    # df = filter_df_by_filters(df, filters)
    print("[DEBUG] After filtering:", df.shape)

    return df.to_dict("records")

@callback(Output("selected-topic", "data"),
          Input("bar-topics", "clickData"),
          Input("pie-topics", "clickData"))

def store_topic(bar_click, pie_click):
    if bar_click:
        return bar_click["points"][0]["label"]
    if pie_click:
        return pie_click["points"][0]["label"]
    return None

