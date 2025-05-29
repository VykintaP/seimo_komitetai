from dash import Dash, html, Input, Output, State, callback, dash_table
from visualize.committee_donut import get_donut_layout
from visualize.theme_distribution import get_theme_distribution_layout
from visualize.committee_profiles import get_committee_profiles_layout
from visualize.theme_distribution import df_all

app = Dash(__name__)
app.title = "Ką veikia Seimo komitetai?"

app.layout = html.Div([
    html.H1("Seimo temų analizė", style={"color": "#2C3E50"}),
    get_donut_layout(app),
    get_theme_distribution_layout(),
    get_committee_profiles_layout()

])
@callback(
    Output("tabs", "value"),
    Output("selected-theme", "data"),
    Input("theme-bar", "clickData"),
    prevent_initial_call=True
)
def update_on_click(clickData):
    if clickData:
        theme = clickData["points"][0]["y"]
        return "questions", theme
    return dash.no_update, dash.no_update


@callback(
    Output("questions-container", "children"),
    Input("selected-theme", "data")
)
def display_questions(theme):
    if not theme:
        return html.P("Pasirink tema grafike.")

    df_filtered = df_all[df_all["tema"] == theme][["data", "klausimas"]]
    return dash_table.DataTable(
        columns=[{"name": i.capitalize(), "id": i} for i in df_filtered.columns],
        data=df_filtered.to_dict("records"),
        page_size=20,
        style_table={"overflowX": "auto"},
        style_cell={"textAlign": "left"},
    )


if __name__ == "__main__":
    app.run(debug=True)

from scripts.load_to_sql import main as load_to_sql_main
load_to_sql_main()
