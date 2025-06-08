import plotly.graph_objects as go
import pandas as pd

def get_heatmap(df, selected_topic=None):
    if df.empty:
        return go.Figure()

    pivot_table = df.pivot_table(index="komitetas", columns="tema", values="klausimas", aggfunc="count", fill_value=0)

    fig = go.Figure(
        data=go.Heatmap(
            z=pivot_table.values,
            x=pivot_table.columns,
            y=pivot_table.index,
            colorscale="Reds"
        )
    )

    fig.update_layout(
        margin=dict(t=50, b=50, l=50, r=50),
        xaxis_nticks=36,
        yaxis=dict(title="Komitetas"),
        xaxis=dict(title="Tema"),
    )
    return fig
