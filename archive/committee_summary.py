from dash import dash_table, html

from config import TABLE_CLASSIFIED
from visualize.utils.db import query_df


def get_committee_summary():
    query = f"""
        SELECT
            komitetas,
            COUNT(*) AS klausimai,
            COUNT(DISTINCT data) AS unikalios_datos,
            ROUND(COUNT(*) * 1.0 / COUNT(DISTINCT data), 2) AS vid_klausimu_per_poseidi
        FROM {TABLE_CLASSIFIED}
        GROUP BY komitetas
        ORDER BY klausimai DESC
    """
    df = query_df(query)

    df = df.rename(
        columns={
            "komitetas": "Komitetas",
            "klausimai": "Klausimų sk.",
            "unikalios_datos": "Unikalios datos",
            "vid_klausimu_per_poseidi": "Vid. klausimų / posėdį",
        }
    )

    return html.Div(
        [
            html.H3("Komitetų veiklos santrauka", style={"color": "#2C3E50"}),
            dash_table.DataTable(
                columns=[{"name": i, "id": i} for i in df.columns],
                data=df.to_dict("records"),
                style_table={"overflowX": "auto"},
                style_cell={"padding": "5px", "textAlign": "left"},
                style_header={"backgroundColor": "#F5F7FA", "fontWeight": "bold"},
            ),
        ]
    )
