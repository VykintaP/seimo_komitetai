import pandas as pd

def filter_df_by_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if not filters:
        return df

    start = filters.get("start", "1900-01-01")
    end = filters.get("end", "2100-01-01")
    committees = filters.get("committees", [])

    df = df[(df["data"] >= start) & (df["data"] <= end)]

    if committees:
        df = df[df["komitetas"].isin(committees)]

    return df
