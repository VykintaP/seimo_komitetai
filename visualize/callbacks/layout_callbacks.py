import logging
import traceback
import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, State, callback, ctx, dcc, html, no_update

import visualize.components.bar_committees as bar_committees
import visualize.components.kpi_cards as kpi_cards
import visualize.components.pie_topics as pie_topics
import visualize.components.questions_table as table_module
from visualize.components.line_topics import get_line_figure
from visualize.utils.topic_labels import TOPIC_LABELS

# Nustatome loginimą pirminiu lygiu
logging.basicConfig(level=logging.INFO)

# Patvirtinimas, kad modulis veikia
print("[DEBUG] layout_callbacks.py perrašytas – dashboard-content aktyvus")


@callback(
    Output("dashboard-content", "children"),
    Input("filtered-df", "data"),
    Input("selected-topic", "data"),
    Input("selected-committee", "data"),
    Input("selected-date", "data"),
    Input("raw-data", "data"),
    Input("filtered-bar-data", "data"),
)
def render_dashboard(
        filtered_data,
        selected_topic,
        selected_committee,
        selected_date,
        raw_data,
        filtered_bar_data,
):
    """Atvaizduoja pagrindinį valdymo skydelį su grafikais ir lentele"""
    try:
        if filtered_data:
            df = pd.DataFrame(filtered_data)
            raw_df = pd.DataFrame(raw_data)
        else:
            # Tuščia lentelė, kai nėra duomenų
            df = pd.DataFrame(
                columns=[
                    "komitetas",
                    "data",
                    "klausimas",
                    "tema",
                    "projektas",
                    "atsakingi",
                    "dalyviai",
                ]
            )
    except Exception as e:
        logging.error(f"[KLAIDA] Nepavyko konvertuoti į DataFrame: {e}")
        traceback.print_exc()
        return html.Div("Klaida apdorojant duomenis.")

    if df.empty:
        return html.Div([html.H4("Nėra duomenų pagal pasirinktus filtrus.")])

    if not df.empty and pd.to_datetime(df["data"], errors="coerce").dropna().empty:
        return html.Div([
            html.H4("Nėra datų pasirinkimui pagal pasirinktus filtrus."),
            html.P("Pabandykite pasirinkti kitą temą ar komitetą."),
        ])

    df_filtered = df.copy()

    # Pritaikome pasirinktus filtrus
    if selected_committee:
        df_filtered = df_filtered[df_filtered["komitetas"] == selected_committee]

    if selected_topic:
        df_filtered = df_filtered[df_filtered["tema"] == selected_topic]

    try:
        # Formuojame vizualizacijas
        bar_fig = bar_committees.get_committees_bar(
            pd.DataFrame(filtered_bar_data), selected_committee
        )
        pie_fig = pie_topics.get_pie_figure(
            df_filtered, selected_topic, selected_committee
        )
        line_fig = get_line_figure(df_filtered, selected_topic, selected_date)

    except Exception as e:
        logging.error(f"[KLAIDA] Generuojant grafikus: {e}")
        return html.Div("Klaida generuojant grafikus.")

    # Grąžiname valdymo skydelio komponentus
    return [
        html.Div(
            className="grid-span-12",
            children=[kpi_cards.generate_kpi_cards(df_filtered)],
        ),
        html.Div(
            className="display-grid-two grid-span-12",
            children=[
                html.Div(
                    className="card-fixed",
                    children=[
                        html.H4(
                            "Komitetai pagal svarstytų klausimų kiekį",
                            className="card-title",
                        ),
                        dcc.Graph(
                            id="bar-committees",
                            figure=bar_fig,
                            config={"displayModeBar": False},
                            style={"height": "460px"},
                        ),
                    ],
                ),
                html.Div(
                    className="card-fixed",
                    children=[
                        html.H4(
                            "Temų pasiskirstymas – apie ką svarsto Seimo komitetai",
                            className="card-title",
                        ),
                        dcc.Graph(
                            id="pie-topics",
                            figure=pie_fig,
                            config={"displayModeBar": False},
                            style={"height": "460px"},
                        ),
                    ],
                ),
            ],
        ),
        html.Div(
            className="grid-span-12 chart-card",
            children=[
                html.Div(
                    className="card",
                    children=[
                        html.H4(
                            "Klausimų skaičius per savaitę", className="card-title"
                        ),
                        dcc.Graph(
                            id="line-topics",
                            figure=line_fig,
                            style={"height": "420px", "width": "100%"},
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            className="grid-span-12",
            children=[
                html.Div(
                    className="card",
                    children=[
                        html.H4("Darbotvarkės klausimai", className="card-title"),
                        table_module.get_questions_table(
                            df_filtered,
                            selected_topic,
                            selected_committee,
                            selected_date,
                        ),
                    ],
                )
            ],
        ),
    ]


@callback(
    Output("active-filters", "children"),
    Input("selected-committee", "data"),
    Input("selected-topic", "data"),
    Input("selected-date", "data"),
)
def update_active_filters(committee, topic, date):
    """Atnaujina aktyvių filtrų juostą"""
    badges = []

    # Komiteto filtro žymė
    if committee:
        badges.append(html.Span(f"Komitetas: {committee}", className="filter-badge"))
    else:
        badges.append(html.Span("Komitetas: Visi komitetai", className="filter-badge"))

    # Temos filtro žymė
    if topic:
        topic_lt = TOPIC_LABELS.get(topic, topic)
        badges.append(html.Span(f"Tema: {topic_lt}", className="filter-badge"))
    else:
        badges.append(html.Span("Tema: Visos temos", className="filter-badge"))

    # Datos filtro žymė
    if date and isinstance(date, str) and date.strip() != "RESET":
        dt = pd.to_datetime(date)
        date_str = dt.strftime("%Y-%m-%d")
        badges.append(
            html.Span(f"Laikotarpis: {date_str} ±3 d.", className="filter-badge")
        )
    else:
        badges.append(html.Span("Laikotarpis: Visas", className="filter-badge"))

    return badges


@callback(
    Output("selected-committee", "data"),
    Output("selected-topic", "data"),
    Output("selected-date", "data"),
    Output("date-picker-range", "start_date"),
    Output("date-picker-range", "end_date"),
    Input("bar-committees", "clickData"),
    Input("pie-topics", "clickData"),
    Input("line-topics", "clickData"),
    Input("clear-filters-btn", "n_clicks"),
    State("selected-committee", "data"),
    State("selected-topic", "data"),
    State("selected-date", "data"),
    prevent_initial_call=True,
)
def central_filter_handler(
        bar_click,
        pie_click,
        line_click,
        clear_click,
        current_committee,
        current_topic,
        current_date,
):
    """Centralizuotas filtrų valdymas pagal vartotojo veiksmus"""
    triggered_id = ctx.triggered_id

    # Filtrų išvalymas
    if triggered_id == "clear-filters-btn":
        return None, None, None, None, None

    # Komiteto filtravimas
    if triggered_id == "bar-committees" and bar_click:
        clicked = bar_click["points"][0]["y"]  # BarChart yra horizontalus
        corrected_committee = f"{clicked.strip()} komitetas"

        print(f"[DEBUG] Paspaustas trumpas: {clicked}")
        print(f"[DEBUG] Atstatytas pilnas: {corrected_committee}")

        if corrected_committee == current_committee:
            return None, current_topic, current_date, no_update, no_update
        return corrected_committee, current_topic, current_date, no_update, no_update

    # Temos filtravimas
    if triggered_id == "pie-topics" and pie_click:
        clicked_topic = pie_click["points"][0]["customdata"]
        if clicked_topic == current_topic:
            return current_committee, None, current_date, no_update, no_update
        return current_committee, clicked_topic, current_date, no_update, no_update

    # Datos filtravimas
    if triggered_id == "line-topics" and line_click:
        clicked_label = line_click["points"][0]["x"]
        try:
            selected_dt = pd.to_datetime(clicked_label.strip())
            new_date = selected_dt.strftime("%Y-%m-%d")
            start_str = (selected_dt - pd.Timedelta(days=3)).strftime("%Y-%m-%d")
            end_str = (selected_dt + pd.Timedelta(days=3)).strftime("%Y-%m-%d")

            if isinstance(current_date, str) and new_date == current_date.strip():
                return current_committee, current_topic, "RESET", None, None

            return current_committee, current_topic, new_date, start_str, end_str
        except Exception as e:
            logging.warning(f"[WARN] Nepavyko interpretuoti datos iš line chart: {e}")
            return current_committee, current_topic, current_date, no_update, no_update

    return current_committee, current_topic, current_date, no_update, no_update
