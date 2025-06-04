from dash import dcc, Input, Output, callback, html, State
import pandas as pd
import logging
import visualize.components.bar_committees as bar_committees

import visualize.components.filters as filters_module
import visualize.components.bar_topics as bar_topics
import visualize.components.pie_topics as pie_topics
import visualize.components.line_topics as line_topics
import visualize.components.questions_table as table_module

logging.basicConfig(level=logging.INFO)


@callback(
    Output("tab-content", "children"),
    Input("main-tabs", "value"),
    Input("filtered-df", "data"),
    Input("selected-topic", "data"),
    State("committee-filter", "data")
)
def render_tab(tab, filtered_data, selected_topic, selected_committee):
    print("[DEBUG] tab =", tab)

    if filtered_data:
        df = pd.DataFrame(filtered_data)
    else:
        df = pd.DataFrame(columns=[
            "komitetas", "data", "klausimas", "tema",
            "projektas", "atsakingi", "dalyviai"
        ])

    print("[DEBUG] df.shape =", df.shape)
    print("[DEBUG] columns =", df.columns.tolist())
    print("[DEBUG] render_tab() triggered")

    if tab == "dashboard":
        if not df.empty and selected_committee is None:
            return html.Div(className="grid-2", children=[
                html.Div(className="card", children=[
                    html.H4("Klausimai pagal komitetą"),
                    dcc.Graph(id="bar-committees", figure=bar_committees.get_committees_bar(df))
                ]),
                html.Div(className="card", children=[
                    html.H4("Temų proporcijos"),
                    dcc.Graph(id="donut-topics", figure=pie_topics.get_pie_figure(df, None))
                ])
            ])

        if not df.empty and "tema" in df.columns:
            bar_fig = bar_topics.get_bar_figure(df, selected_topic)
            pie_fig = pie_topics.get_pie_figure(df, selected_topic)
            line_fig = line_topics.get_line_figure(df, selected_topic)
        else:
            bar_fig = {}
            pie_fig = {}
            line_fig = {}

        return html.Div([

            html.Div(className="responsive-grid", children=[
                html.Div(className="card", children=[
                    html.H4("Temų dažnumas"),
                    dcc.Graph(id="bar-topics", figure=bar_fig)
                ]),
                html.Div(className="card", children=[
                    html.H4("Temų proporcijos"),
                    dcc.Graph(id="pie-topics", figure=pie_fig)
                ]),
            ]),

            html.Div(className="grid-2", children=[
                html.Div(className="card", children=[
                    html.H4("Klausimų sąrašas"),
                    table_module.get_questions_table(df, selected_topic)
                ]),
                html.Div(className="card", children=[
                    html.H4("Tema laikui bėgant"),
                    dcc.Graph(id="line-topics", figure=line_fig)
                ]),
            ]),
        ])

    elif tab == "info":
        return html.Div([
            html.H3("Info"),
            html.P("Čia bus paaiškinimai apie projekto architektūrą, duomenis ir kt.")
        ])

    logging.warning(f"[WARNING] Nepažįstamas tab: {tab}")
    return html.Div([html.P("Nepažįstamas skirtukas")])
