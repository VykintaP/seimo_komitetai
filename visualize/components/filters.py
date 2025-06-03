from dash import html, dcc

def get_filters():
    return html.Div(className="grid-filters", children=[
        dcc.Dropdown(
            id="committee-filter",
            options=[
                {"label": "Biudžeto ir finansų komitetas", "value": "Biudžeto ir finansų komitetas"},
                {"label": "Teisės ir teisėtvarkos komitetas", "value": "Teisės ir teisėtvarkos komitetas"}
            ],
            multi=True,
            placeholder="Pasirink komitetą",
            className="dropdown"
        ),
        dcc.DatePickerRange(
            id="date-filter",
            min_date_allowed="2020-01-01",
            max_date_allowed="2025-12-31",
            start_date="2020-01-01",  # <— pradžia
            end_date="2025-12-31",
            start_date_placeholder_text="Nuo",
            end_date_placeholder_text="Iki"
        )
    ])


