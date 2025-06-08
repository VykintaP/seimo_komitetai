import pandas as pd

def filter_df_by_filters(df: pd.DataFrame, filters: dict) -> pd.DataFrame:
    if df.empty:
        return df

    if not pd.api.types.is_datetime64_any_dtype(df["data"]):
        df["data"] = pd.to_datetime(df["data"], errors="coerce")

    # Filtrai: data
    start = filters.get("start")
    end = filters.get("end")

    if start:
        df = df[df["data"] >= pd.to_datetime(start)]
    if end:
        df = df[df["data"] <= pd.to_datetime(end)]

    # Filtras: komitetai
    committees = filters.get("committees")
    if committees:
        df = df[df["komitetas"].isin(committees)]

    # Filtras: temos
    topics = filters.get("topics")
    if topics:
        df = df[df["tema"].isin(topics)]

    return df
