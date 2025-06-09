from dash import Input, Output, callback

from config import TABLE_CLASSIFIED
from visualize.utils.db import query_df


@callback(
    Output("committee-filter", "options"),
    Input("filters-store", "data"),  # paleidžia pirmą kartą renderinant
)
def populate_committee_options(_):
    df = query_df(
        f"SELECT DISTINCT komitetas FROM {TABLE_CLASSIFIED} WHERE komitetas IS NOT NULL"
    )
    options = [{"label": val, "value": val} for val in sorted(df["komitetas"].unique())]
    return options
