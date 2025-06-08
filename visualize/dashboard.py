from dash import Dash, dcc, html, Input, Output
from visualize.layout import serve_layout
from info_layout import info_layout
import callbacks.layout_callbacks
import callbacks.filter_callbacks


app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    title="Seimo komitetų radaras"
)


app.layout = html.Div([
    dcc.Location(id="url", refresh=False),
    html.Div(id="page-content")
])

@app.callback(
    Output("page-content", "children"),
    Input("url", "pathname")
)
def display_page(pathname):
    if pathname == "/info":
        return info_layout
    return serve_layout()

if __name__ == "__main__":

    app.run(debug=True, port=8051)