import pandas as pd
from pathlib import Path

def summarize_cleaned_data():
    cleaned_dir = Path(__file__).resolve().parents[1] / "data" / "cleaned"
    files = list(cleaned_dir.glob("*.csv"))

    summary = []
    for filepath in files:
        df = pd.read_csv(filepath)
        required_cols = {"date", "question", "committee"}
        if not required_cols.issubset(df.columns):
            continue
        name = filepath.stem.replace("_", " ").title()

        num_questions = len(df)
        empty_questions = df['question'].isna().sum() + df['question'].eq("").sum()
        empty_dates = df['date'].isna().sum() + df['date'].eq("").sum()


        try:
            date_parsed = pd.to_datetime(df['date'], errors='coerce')
        except Exception:
            date_parsed = pd.Series([pd.NaT] * len(df))

        start_date = date_parsed.min()
        end_date = date_parsed.max()
        duration_days = (end_date - start_date).days or 1
        questions_per_day = round(num_questions / duration_days, 2)
        questions_per_week = round(questions_per_day * 7, 2)

        unique_dates = date_parsed.dropna().nunique()
        avg_questions_per_date = round(num_questions / unique_dates, 2) if unique_dates else 0

        flag = ""
        if unique_dates <= 3:
            flag = "mažai posėdžių"
        elif avg_questions_per_date > 15:
            flag = "⚠ \\daug klausimų viename posėdyje"

        summary.append({
            "committee": name,
            "questions": num_questions,
            "empty_questions": empty_questions,
            "empty_dates": empty_dates,
            "date_range": f"{start_date.date()} – {end_date.date()}" if pd.notna(start_date) and pd.notna(end_date) else "Nenurodyta",
            "unique_dates": unique_dates,
            "questions/week": questions_per_week,
            "avg_q_per_date": avg_questions_per_date,
            "flag": flag
        })

    summary_df = pd.DataFrame(summary).sort_values(by="questions", ascending=False)

    print("KOMITETŲ ANALIZĖ:")
    print(summary_df.to_string(index=False))

    print("Apibendrinimas:")
    print(f"- Iš viso komitetų: {len(files)}")
    print(f"- Bendrai klausimų: {summary_df['questions'].sum()}")
    print(f"- Daugiausia klausimų: {summary_df.iloc[0]['committee']} ({summary_df.iloc[0]['questions']})")
    print(f"- Mažiausiai klausimų: {summary_df.iloc[-1]['committee']} ({summary_df.iloc[-1]['questions']})")

if __name__ == "__main__":
    summarize_cleaned_data()


from visualize.plots import plot_questions_per_week
plot_questions_per_week()
