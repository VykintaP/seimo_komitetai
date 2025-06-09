from pathlib import Path

import pandas as pd


def test_classified_data_quality():
    classified_dir = Path("data/classified")
    files = list(classified_dir.glob("*.csv"))
    assert files, "Nėra failų kataloge data/classified"

    all_topics = []
    for file in files:
        df = pd.read_csv(file)
        assert "question" in df.columns
        assert "predicted_topic_lt" in df.columns
        assert "confidence_score" in df.columns

        assert not df["question"].isna().all(), f"{file.name}: visi question tušti"
        assert (
            not df["predicted_topic_lt"].isna().all()
        ), f"{file.name}: visos temos tuščios"
        assert (
            df["confidence_score"] > 0.3
        ).any(), f"{file.name}: visos confidence < 0.3"

        all_topics.extend(df["predicted_topic_lt"].dropna().tolist())

    topic_series = pd.Series(all_topics)
    top_counts = topic_series.value_counts()
    top_ratio = top_counts.iloc[0] / len(topic_series)
    assert (
        top_ratio < 0.7
    ), f"Dominuoja viena tema: '{top_counts.index[0]}' ({top_ratio:.2%})"
