from dash import dcc, Input, Output, callback, html
import pandas as pd

import visualize.components.filters as filters_module
import visualize.components.bar_topics as bar_module
import visualize.components.pie_topics as pie_module
import visualize.components.line_topics as line_module
import visualize.components.questions_table as table_module

@callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
    Input("filtered-df", "data"),
    Input("selected-topic", "data")
)
def render_tab(tab, filtered_data, selected_topic):
    df = pd.DataFrame(filtered_data) if filtered_data else pd.DataFrame()

    if tab == "dashboard":
        return html.Div([
        filters_module.get_filters(),
        html.Div(className="grid-2", children=[
            dcc.Graph(id="bar-topics", figure=bar_module.get_bar_figure(df, selected_topic)),
            dcc.Graph(id="pie-topics", figure=pie_module.get_pie_figure(df, selected_topic))
        ]),
        dcc.Graph(id="line-topics", figure=line_module.get_line_figure(df, selected_topic)),
        table_module.get_questions_table(df, selected_topic)
    ])

    elif tab == "info":
        return html.Div([
            html.H3("Info"),
            html.P("Čia bus paaiškinimai apie projekto architektūrą, duomenis ir kt.")
        ])
    print(f"[DEBUG] render_tab: tab={tab}, rows={len(df)}, selected_topic={selected_topic}")

    return html.Div([html.P("Nepažįstamas skirtukas")])

import visualize.callbacks.filter_callbacks

