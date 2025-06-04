import pandas as pd

def filter_df_by_filters(df, filters: dict) -> pd.DataFrame:
    start = filters.get("start")
    end = filters.get("end")

    if start and end:
        df = df[(df["data"] >= start) & (df["data"] <= end)]

    committees = filters.get("committees")
    if committees:
        df = df[df["komitetas"].isin(committees)]

    return df
