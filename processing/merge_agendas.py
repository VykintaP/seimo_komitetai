import pandas as pd
from pathlib import Path

def merge_agendas():
    data_dir = Path(__file__).resolve().parents[1] / "data"
    output_file = data_dir / "all_agendas.csv"
    csv_files = list(data_dir.glob("*_komitetas.csv"))

    if not csv_files:
        print("Nerasta failų su _komitetas.csv pavadinimu.")
        return pd.DataFrame()

    all_dfs = []
    for file in csv_files:
        try:
            df = pd.read_csv(file)
            df = df[["date", "question", "committee"]]
            all_dfs.append(df)
        except Exception as e:
            print(f"Klaida su {file.name}: {e}")

    final_df = pd.concat(all_dfs, ignore_index=True)
    output_file.parent.mkdir(parents=True, exist_ok=True)
    final_df.to_csv(output_file, index=False, encoding="utf-8")
    print(f"Išsaugota: {output_file.name} ({len(final_df)} įrašų)")

    return final_df
