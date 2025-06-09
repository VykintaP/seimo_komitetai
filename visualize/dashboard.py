# Pagrindinis Dash aplikacijos modulis

import callbacks.filter_callbacks
import callbacks.layout_callbacks
from dash import Dash, Input, Output, dcc, html
from info_layout import info_layout

from visualize.layout import serve_layout

app = Dash(
    __name__,
    suppress_callback_exceptions=True,
    prevent_initial_callbacks=True,
    title="Seimo komitetų radaras",
)

app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)


@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    """Grąžina tinkamą puslapio turinį pagal URL kelią"""
    if pathname == "/info":
        return info_layout
    return serve_layout()


if __name__ == "__main__":
    # Paleidžiame aplikaciją debug režimu
    app.run(debug=True, port=8051)
