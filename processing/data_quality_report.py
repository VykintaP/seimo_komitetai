import pandas as pd
from pathlib import Path

CLEANED_DIR = Path(__file__).resolve().parents[1] / "data" / "diagnostics"
REPORT_PATH = CLEANED_DIR / "quality_report.csv"

def analyze_file(filepath):
    df = pd.read_csv(filepath)
    report = {}
    report["committee"] = filepath.name.replace("_clean.csv", "").replace("_", " ").title()
    lengths = df["question"].astype(str).apply(len)
    report["min_length"] = lengths.min()
    report["max_length"] = lengths.max()
    report["mean_length"] = round(lengths.mean(), 2)
    report["median_length"] = lengths.median()
    report["total_questions"] = len(df)
    report["too_short"] = (lengths < 20).sum()
    report["too_short_percent"] = round(report["too_short"] / len(df) * 100, 2)
    words = df["question"].astype(str).str.lower().str.split()
    unique_words = set(word for sublist in words for word in sublist)
    report["unique_words"] = len(unique_words)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    future_dates = df["date"] > pd.Timestamp.today()
    report["future_dates"] = future_dates.sum()
    report["future_percent"] = round(future_dates.mean() * 100, 2)
    return report

def main():
    results = []
    for file in CLEANED_DIR.glob("*_clean.csv"):
        results.append(analyze_file(file))
    df_report = pd.DataFrame(results)
    df_report.to_csv(REPORT_PATH, index=False)
    print(f"Data quality report saved to: {REPORT_PATH}")

if __name__ == "__main__":
    main()
