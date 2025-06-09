def plot_questions_per_week():
    from pathlib import Path

    import matplotlib.pyplot as plt
    import pandas as pd
    import seaborn as sns

    cleaned_dir = Path(__file__).resolve().parents[1] / "data" / "cleaned"
    files = list(cleaned_dir.glob("*.csv"))

    summary = []
    for filepath in files:
        df = pd.read_csv(filepath)
        if not {"date", "question", "committee"}.issubset(df.columns):
            continue

        name = filepath.stem.replace("_", " ").title()
        date_parsed = pd.to_datetime(df["date"], errors="coerce")
        start_date = date_parsed.min()
        end_date = date_parsed.max()

        if pd.isna(start_date) or pd.isna(end_date) or end_date <= start_date:
            continue

        duration_days = (end_date - start_date).days or 1
        questions_per_day = len(df) / duration_days
        questions_per_week = round(questions_per_day * 7, 2)

        summary.append({"committee": name, "questions/week": questions_per_week})

    if not summary:
        print("⚠ Nerasta duomenų vizualizacijai.")
        return

    df_summary = pd.DataFrame(summary).sort_values("questions/week", ascending=False)

    plt.figure(figsize=(12, 7))
    sns.barplot(data=df_summary, x="questions/week", y="committee", palette="Blues_d")
    plt.title("Klausimų per savaitę skaičius pagal komitetą")
    plt.xlabel("Klausimai per savaitę")
    plt.ylabel("Komitetas")
    plt.tight_layout()
    plt.show()
