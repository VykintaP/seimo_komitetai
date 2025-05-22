import pandas as pd
from dash import Dash, dcc, html
import plotly.express as px
from pathlib import Path

app = Dash(__name__)

def load_summary():
    cleaned_dir = Path(__file__).resolve().parents[1] / "data" / "cleaned"
    files = list(cleaned_dir.glob("*.csv"))

    summary = []
    for filepath in files:
        df = pd.read_csv(filepath)
        if not {"date", "question", "committee"}.issubset(df.columns):
            continue

        name = filepath.stem.replace("_", " ").title()
        dates = pd.to_datetime(df["date"], errors="coerce")
        start, end = dates.min(), dates.max()
        if pd.isna(start) or pd.isna(end) or end <= start:
            continue

        duration_days = (end - start).days or 1
        questions_per_week = round(len(df) / duration_days * 7, 2)

        summary.append({"committee": name, "questions_per_week": questions_per_week})

    return pd.DataFrame(summary)

df = load_summary()
fig = px.bar(df.sort_values("questions_per_week", ascending=False),
             x="questions_per_week", y="committee", orientation="h",
             labels={"questions_per_week": "Klausimai per savaitę", "committee": "Komitetas"},
             title="Klausimų per savaitę intensyvumas")

fig.update_layout(yaxis=dict(autorange="reversed"))

app.layout = html.Div([
    html.H2("Komitetų klausimų intensyvumo analizė"),
    dcc.Graph(figure=fig)
])

if __name__ == "__main__":
    app.run(debug=True)
