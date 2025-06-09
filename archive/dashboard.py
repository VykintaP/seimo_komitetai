import pandas as pd
from dash import Dash, Input, Output, State, dcc, html

from archive.committee_chart import get_committee_chart
from archive.committee_summary import get_committee_summary
from archive.wordcloud_component import get_wordcloud_component
from visualize.components.filters import get_filters
from visualize.layout import serve_layout

app.layout = serve_layout

app = Dash(__name__, suppress_callback_exceptions=True)

app.layout = html.Div(
    className="main-container",
    children=[
        dcc.Store(id="filtered-df"),  # <- čia buvo trūkstamas kablelis
        html.H1("Seimo komitetų darbotvarkių analizė", style={"color": "#2C3E50"}),
        dcc.Tabs(
            id="main-tabs",
            value="overview",
            children=[
                dcc.Tab(label="Apžvalga", value="overview"),
                dcc.Tab(label="Žodžių debesis", value="wordcloud"),
                dcc.Tab(label="Temų analizė", value="themes"),
                dcc.Tab(label="Duomenų lentelė", value="table"),
                dcc.Tab(label="Kokybės patikra", value="quality"),
            ],
        ),
        html.Div(id="tab-content"),
    ],
)


@app.callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
    State("filtered-df", "data"),
)
def render_tab(tab, data):
    df = pd.DataFrame(data) if data else pd.DataFrame()

    if tab == "overview":
        return html.Div([get_filters(), get_committee_chart(), get_committee_summary()])
    elif tab == "wordcloud":
        return get_wordcloud_component(df)
    elif tab == "themes":
        return html.Div([html.H3("Temų analizė")])
    elif tab == "table":
        return html.Div([html.H3("Duomenų lentelė")])
    elif tab == "quality":
        return html.Div([html.H3("Klasifikavimo kokybė")])
    return html.Div([html.H3("Nepasirinktas tabas")])


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1")
