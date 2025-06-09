import plotly.express as px
from dash import Input, Output, callback, dash_table, dcc, html

from config import TABLE_CLASSIFIED
from visualize.utils.db import query_df


# 1) Iškvietimas, kai paspaudžiamas komitetas grafike
@callback(Output("selected-committee", "data"), Input("committee-bar", "clickData"))
def store_selected_committee(clickData):
    if clickData:
        return clickData["points"][0]["y"]
    return None


# 2) Iškvietimas, kai pasikeičia pasirinktasis komitetas ar filtrai
@callback(
    Output("theme-by-committee", "children"),
    Input("selected-committee", "data"),
    Input("filters-store", "data"),
    prevent_initial_call=True,
)
def update_theme_chart(committee, filters):
    if not committee:
        return html.P("Pasirink komitetą grafike.")

    start = filters.get("start", "1900-01-01")
    end = filters.get("end", "2100-01-01")

    sql = f"""
        SELECT komitetas, tema, data, klausimas FROM {TABLE_CLASSIFIED}
        WHERE komitetas = ?
        AND date(data) BETWEEN date(?) AND date(?)
    """
    df = query_df(sql, (committee, start, end))

    if df.empty:
        return html.P("Pasirinktam laikotarpiui nėra duomenų.")

    theme_counts = df["tema"].value_counts().reset_index()
    theme_counts.columns = ["Tema", "Klausimų skaičius"]

    fig = px.bar(
        theme_counts,
        x="Klausimų skaičius",
        y="Tema",
        orientation="h",
        title=f"Temos komitete: {committee}",
    )
    fig.update_traces(hovertemplate="%{y}: %{x} klausimų")

    klausimai_df = df[["data", "klausimas"]].copy()

    return html.Div(
        [
            dcc.Graph(figure=fig),
            html.H4(f"Klausimai komitete: {committee}", style={"marginTop": "20px"}),
            dash_table.DataTable(
                columns=[
                    {"name": "Data", "id": "data"},
                    {"name": "Klausimas", "id": "klausimas"},
                ],
                data=klausimai_df.to_dict("records"),
                page_size=15,
                style_table={"overflowX": "auto"},
                style_cell={"textAlign": "left"},
            ),
        ]
    )
