import base64
from io import BytesIO
import pandas as pd
from wordcloud import WordCloud
from dash import html

def get_wordcloud_component(df: pd.DataFrame) -> html.Div:
    if df.empty or "tema" not in df.columns:
        return html.Div("Nėra temų duomenų debesims generuoti.", className="card")

    # Temos jungiamos, kad WordCloud jų neskaldytų
    joined_themes = df["tema"].dropna().astype(str).str.replace(" ", "_")
    text = " ".join(joined_themes)

    if not text.strip():
        return html.Div("Temų tekstas tuščias.", className="card")

    wc = WordCloud(width=600, height=300, background_color="white", colormap="Dark2").generate(text)

    img_io = BytesIO()
    wc.to_image().save(img_io, format="PNG")
    encoded = base64.b64encode(img_io.getvalue()).decode()

    return html.Div([
        html.H3("Dažniausios temos", style={"color": "#2C3E50"}),
        html.Img(src=f"data:image/png;base64,{encoded}", style={"maxWidth": "100%"})
    ], className="card", style={"padding": "20px"})
