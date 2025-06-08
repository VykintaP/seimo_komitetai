import plotly.graph_objects as go
import pandas as pd
from visualize.utils.topic_labels import TOPIC_LABELS

LINE_CHART_GRADIENT = [
    "#FCFFDD", "#FAFDCB", "#F9EDB9", "#F8DDA5", "#F6CD91",
    "#F5BD7D", "#F4AD69", "#F39D55", "#F18D41", "#F07D2D",
    "#EF6D19", "#DE6719", "#CE6018", "#BD5A18", "#AD5317",
    "#9D4D17", "#8C4616", "#7B4016", "#6A3915", "#593315"
]

def get_line_figure(df: pd.DataFrame, selected_topic: str = None, selected_date: str = None) -> go.Figure:
    try:
        if df is None or df.empty or "data" not in df.columns or "tema" not in df.columns:
            return go.Figure()

        # Paruošiame datą
        df["data"] = pd.to_datetime(df["data"], errors="coerce")
        df = df.dropna(subset=["data"])

        # Filtravimas pagal temą
        if selected_topic:
            df = df[df["tema"] == selected_topic]


        # Grupavimas pagal savaitės pradžią
        df["savaite_nuo"] = df["data"] - pd.to_timedelta(df["data"].dt.weekday, unit="d")
        df["savaite_nuo"] = df["savaite_nuo"].dt.date  # ← Pašalina laiką, palieka tik datą

        grouped = df.groupby("savaite_nuo").size().reset_index(name="Klausimų skaičius")
        x_label = "Savaitės pradžia"
        hover_label = "%{x|%Y-%m-%d}"



        if grouped.empty:
            return go.Figure()

        # Spalvos pagal kiekį
        min_val = grouped["Klausimų skaičius"].min()
        max_val = grouped["Klausimų skaičius"].max()
        val_range = max_val - min_val if max_val > min_val else 1


        yaxis_range = None
        if min_val == max_val or max_val <= 3:
            yaxis_range = [0, max_val + 1]

        def map_color(value):
            idx = int((value - min_val) / val_range * (len(LINE_CHART_GRADIENT) - 1))
            return LINE_CHART_GRADIENT[idx]

        grouped["spalva"] = grouped["Klausimų skaičius"].apply(map_color)

        bar = go.Bar(
            x=grouped["savaite_nuo"],
            y=grouped["Klausimų skaičius"],
            marker_color=grouped["Klausimų skaičius"].apply(map_color),
            text=grouped["Klausimų skaičius"],
            textposition="outside",
            cliponaxis=False,
            hovertemplate=f"<b>{hover_label}</b><br>Klausimų sk.: %{{y}}<extra></extra>"
        )

        fig = go.Figure(bar)

        fig.update_layout(
            margin=dict(t=40, b=120, l=60, r=20),
            height=600,
            plot_bgcolor="#FAFAFA",
            bargap=0.2,
            title=None,
            xaxis_title=x_label,
            yaxis_title="Klausimų skaičius",
            xaxis=dict(
                tickmode="array",
                tickvals=grouped.iloc[:, 0],
                ticktext=grouped.iloc[:, 0],
                tickangle=-45,
                tickfont=dict(size=12)
            ),
            yaxis=dict(
                title="Klausimų skaičius",
                range=yaxis_range  # ← čia pritaikytas dugno pakėlimas
            )
        )

        return fig

    except Exception as e:
        import logging
        logging.error(f"Error generating time bar chart: {e}")
        return go.Figure()
