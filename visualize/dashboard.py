from dash import Dash
from visualize.layout import serve_layout
import visualize.callbacks.filter_callbacks

app = Dash(__name__, suppress_callback_exceptions=True)

server = app.server
app.layout = serve_layout


if __name__ == "__main__":
    app.run(debug=True)

