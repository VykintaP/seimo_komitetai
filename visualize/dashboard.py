from dash import Dash
from visualize.layout import serve_layout

app = Dash(__name__, suppress_callback_exceptions=True)
app.layout = serve_layout

import visualize.callbacks.layout_callbacks


if __name__ == "__main__":
    app.run(debug=True)

