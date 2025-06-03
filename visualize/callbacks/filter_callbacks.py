from dash import Input, Output, State, callback, ctx
import pandas as pd
from utils.db import query_df
from utils.filtering import filter_df_by_filters
from config import TABLE_CLASSIFIED

@callback(
    Output("filtered-df", "data"),
    Input("main-tabs", "value"),
    State("committee-filter", "value"),
    State("date-filter", "start_date"),
    State("date-filter", "end_date"),
    prevent_initial_call=False
)
def unified_df_loader(tab, committees, start, end):
    if tab != "dashboard":
        return []

    print("[DEBUG] Triggered by:", ctx.triggered_id)
    print("[DEBUG] Filter input:", committees, start, end)

    df = query_df(f"SELECT * FROM {TABLE_CLASSIFIED}")
    df["data"] = pd.to_datetime(df["data"], errors="coerce")  # ← Būtina

    df_filtered = filter_df_by_filters(df, {
        "committees": committees,
        "start": start,
        "end": end
    })

    print("[DEBUG] After filtering:", len(df_filtered))  # ← Dabar jau veikia

    return df_filtered.to_dict("records")
