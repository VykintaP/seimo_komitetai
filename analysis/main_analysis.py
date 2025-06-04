import pandas as pd
from pathlib import Path
import logging
from collections import Counter
import string

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def plot_questions_per_week():
    import matplotlib.pyplot as plt
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
        num_invalid_dates = df["date"].isna().sum() + df["date"].eq("").sum()
        if num_invalid_dates > 0:
            logging.warning(f"{filepath.name}: {num_invalid_dates} neparsivertų datų")

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
    sns.barplot(data=df_summary, x="questions/week", y="committee", hue="committee", legend=False, palette="Blues_d")
    plt.title("Klausimų per savaitę skaičius pagal komitetą")
    plt.xlabel("Klausimai per savaitę")
    plt.ylabel("Komitetas")
    plt.tight_layout()
    plt.show()


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

        date_parsed = pd.to_datetime(df['date'], errors='coerce')
        num_invalid_dates = df['date'].isna().sum() + df['date'].eq("").sum()
        if num_invalid_dates > 0:
            logging.warning(f"{filepath.name}: {num_invalid_dates} neparsivertų datų")

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
            flag = "⚠ daug klausimų viename posėdyje"

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
    diagnostics_path = Path(__file__).resolve().parents[1] / "data" / "diagnostics" / "diagnostics.csv"
    diagnostics_path.parent.mkdir(parents=True, exist_ok=True)
    summary_df.to_csv(diagnostics_path, index=False, encoding="utf-8-sig")

    print("KOMITETŲ ANALIZĖ:")
    print(summary_df.to_string(index=False))

    print("Apibendrinimas:")
    print(f"- Iš viso komitetų: {len(files)}")
    print(f"- Bendrai klausimų: {summary_df['questions'].sum()}")
    print(f"- Daugiausia klausimų: {summary_df.iloc[0]['committee']} ({summary_df.iloc[0]['questions']})")
    print(f"- Mažiausiai klausimų: {summary_df.iloc[-1]['committee']} ({summary_df.iloc[-1]['questions']})")

def most_common_words_filtered(cleaned_dir: Path, stopwords_path: Path, top_n: int = 15):
    diagnostics_dir = Path(__file__).resolve().parents[1] / "data" / "diagnostics"
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    stop_words = set(word.strip() for word in stopwords_path.open(encoding="utf-8"))
    files = list(cleaned_dir.glob("*.csv"))
    results = []

    for filepath in files:
        df = pd.read_csv(filepath)
        if "question" not in df.columns:
            continue

        all_words = " ".join(df["question"].dropna().astype(str)).lower()
        all_words = all_words.translate(str.maketrans("", "", string.punctuation))
        words = [w for w in all_words.split() if len(w) > 3 and not w.startswith("www") and w not in stop_words]
        counter = Counter(words)
        top_words = counter.most_common(top_n)

        results.append({
            "komitetas": filepath.stem.replace("_", " "),
            "filtruoti žodžiai": ", ".join(f"{w} ({c})" for w, c in top_words)
        })

    df_result = pd.DataFrame(results)
    df_result.to_csv(diagnostics_dir / "words_by_committee_cleaned.csv", index=False, encoding="utf-8-sig")
    print("[OK] Išvalyti žodžiai išsaugoti į words_by_committee_cleaned.csv")

def most_common_words_by_committee(cleaned_dir: Path, top_n: int = 15):
    files = list(cleaned_dir.glob("*.csv"))
    results = []

    diagnostics_dir = Path(__file__).resolve().parents[1] / "data" / "diagnostics"
    diagnostics_dir.mkdir(parents=True, exist_ok=True)

    for filepath in files:
        df = pd.read_csv(filepath)
        if "question" not in df.columns:
            continue

        all_words = " ".join(df["question"].dropna().astype(str)).lower()
        all_words = all_words.translate(str.maketrans("", "", string.punctuation))
        words = [w for w in all_words.split() if len(w) > 3 and not w.startswith("www")]
        counter = Counter(words)
        top_words = counter.most_common(top_n)

        results.append({
            "komitetas": filepath.stem.replace("_", " "),
            "dažniausi žodžiai": ", ".join(f"{w} ({c})" for w, c in top_words)
        })

    df_result = pd.DataFrame(results)
    df_result.to_csv(diagnostics_dir / "words_by_committee.csv", index=False, encoding="utf-8-sig")
    print(df_result)

if __name__ == "__main__":
    summarize_cleaned_data()
    plot_questions_per_week()
    most_common_words_filtered(
        cleaned_dir=Path(__file__).resolve().parents[1] / "data" / "cleaned",
        stopwords_path=Path(__file__).resolve().parents[1] / "stop_words_lt.txt"
    )
    most_common_words_by_committee(Path(__file__).resolve().parents[1] / "data" / "cleaned")