from dash import dcc, html

# Pagrindinis svetainės "Apie" puslapio išdėstymas
info_layout = html.Div(
    className="info-container",
    children=[
        html.H2("Apie projektą"),
        html.P(
            "„Seimo komitetų radaras" ),
        
html.H3("Duomenų šaltiniai"),
html.P(
    [
        "Duomenys automatiškai renkami iš oficialių Seimo komitetų ir plenarinių posėdžių darbotvarkių, "
        "skelbiamų svetainėje ",
        html.A("https://lrs.lt", href="https://lrs.lt", target="_blank"),
    ]
),
html.Hr(),
html.H3("Naudotos technologijos"),
html.Ul(
    [
        html.Li("Programavimo kalba: Python 3.10"),
        html.Li("Bibliotekos: pandas, plotly, scikit-learn, spaCy, flask"),
        html.Li(
            "Vizualizacijos komponentai: Dash (`dcc`, `html`, `dash_table`)"
        ),
        html.Li("Duomenų bazė: SQLite"),
        html.Li(
            "Stilius: `assets/styles.css` (flat dizainas, IBM Plex Sans / Open Sans)"
        ),
    ]
),
html.H3("Kam tai skirta"),
html.Ul(
    [
        html.Li(
            "Tyrėjams ir duomenų analitikams – vertinti Seimo veiklos tendencijas"
        ),
        html.Li(
            "Žurnalistams – rasti faktinę bazę publikacijoms apie politinius procesus"
        ),
        html.Li(
            "Piliečiams ir NVO – stebėti svarstomas temas ir prisidėti prie sprendimų skaidrumo"
        ),
        html.Li(
            "Atvirojo kodo bendruomenei – plėtoti ar pritaikyti projektą savo reikmėms"
        ),
    ]
),
html.H3("Kodo prieinamumas"),
html.P(
    [
        "Projektas vystomas kaip nepriklausoma iniciatyva. ",
        "Kodo bazė viešai prieinama adresu: ",
        html.A(
            "https://github.com/vykinta/seimo-temu-radaras",
            href="https://github.com/vykinta/seimo-temu-radaras",
            target="_blank",
        ),
    ]
),
    # Grįžimo nuoroda į pagrindinį puslapį
dcc.Link("← Grįžti į Seimo komitetų radarą", href="/", className="back-link"),
],
)
