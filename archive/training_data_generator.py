from processing.cleaning_pipeline import clean_question
import pandas as pd
from pathlib import Path

def generate_training_data(input_dir: Path, output_path: Path):
    rows = []
    for file in input_dir.glob("*.csv"):
        df = pd.read_csv(file)
        if "question" not in df.columns:
            continue

        if "topic" not in df.columns and "predicted_topic_lt" in df.columns:
            df["topic"] = df["predicted_topic_lt"]

        for _, row in df.iterrows():
            question = clean_question(str(row.get("question", "")))
            topic = row.get("topic")
            if question and pd.notnull(topic):
                rows.append({"question": question, "topic": topic})
    df_out = pd.DataFrame(rows)
    df_out.to_csv(output_path, index=False)
    return df_out
