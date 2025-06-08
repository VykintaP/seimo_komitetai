from dash import dcc
import plotly.graph_objects as go
import pandas as pd
import logging

BAR_CHART_PALETTE = [
    "#00171A", "#012D24", "#03332D", "#053936", "#063F3F",
    "#084548", "#0D4B51", "#145158", "#1B5760", "#225D67",
    "#29636E", "#307A7C", "#37918A", "#3FA897", "#53B0A1",
    "#67B8AA", "#7BC0B4", "#8FC8BD", "#A3D0C7", "#B6D8D0"
]

logging.basicConfig(level=logging.DEBUG)


def get_committees_bar(df: pd.DataFrame, selected_committee: str = None) -> go.Figure:
    logging.debug(f"[DEBUG] Gauta {len(df)} eilučių BarChart'ui (po filtravimo)")

    if df.empty or "komitetas" not in df.columns:
        fig = go.Figure()
        fig.update_layout(title="Komitetų grafikas – nėra duomenų")
        return fig

    df["komitetas_clean"] = df["komitetas"].str.replace(r"\bkomitetas\b[:\s–-]*", "", case=False,
                                                        regex=True).str.strip()

    all_committees = df["komitetas_clean"].dropna().unique()
    base_counts = pd.DataFrame({"Komitetas": all_committees})

    counts_filtered = df["komitetas_clean"].value_counts().reset_index()
    counts_filtered.columns = ["Komitetas", "Klausimų skaičius"]

    counts = base_counts.merge(counts_filtered, on="Komitetas", how="left").fillna(0)
    counts["Klausimų skaičius"] = counts["Klausimų skaičius"].astype(int)
    counts = counts.head(16)

    selected_committee_cleaned = selected_committee.replace(" komitetas", "").strip() if selected_committee else None

    colors = []
    line_widths = []
    for komitetas in counts["Komitetas"]:
        if selected_committee_cleaned and komitetas == selected_committee_cleaned:
            colors.append("#FFA500")
            line_widths.append(3)
        else:
            colors.append(BAR_CHART_PALETTE[len(colors) % len(BAR_CHART_PALETTE)])
            line_widths.append(1)

    fig = go.Figure(go.Bar(
        x=counts["Klausimų skaičius"],
        y=counts["Komitetas"],
        orientation="h",
        marker=dict(
            color=colors,
            line=dict(color="black", width=line_widths)
        ),
        hovertemplate="<b>%{y}</b><br>Klausimų sk.: %{x}<extra></extra>"
    ))

    fig.update_layout(
        title=None,
        margin=dict(t=30, b=40, l=30, r=30),
        height=500,
        xaxis=dict(
            title=None,
            tickfont=dict(size=12),
            tickangle=0,
            showgrid=True,
            gridcolor="rgba(0,0,0,0.05)",
            zeroline=False,
        ),
        yaxis=dict(
            title=None,
            tickfont=dict(size=13),
            automargin=True,
            categoryorder="total ascending",
            categoryarray=counts["Komitetas"].tolist()[::-1]
        ),
        plot_bgcolor="#FAFAFA",
    )
    return fig


def get_committees_bar_chart(df: pd.DataFrame, selected_committee: str = None):
    fig = get_committees_bar(df, selected_committee)
    return dcc.Graph(figure=fig, id="bar-committees", config={"displayModeBar": False})
