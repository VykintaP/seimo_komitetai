if all_dfs:
    full_df = pd.concat(all_dfs, ignore_index=True)

    # kiek temų neatpažinta
    unknown_count = (full_df["tema"] == "Neatpažinta tema").sum()
    total_count = len(full_df)
    if unknown_count > 0:
        percent = round(unknown_count / total_count * 100, 2)
        print(f"[WARNING] Neatpažinta tema: {unknown_count} klausimų ({percent}%)")

    full_df.to_sql("classified_questions", conn, if_exists="replace", index=False)
    print(f"[OK] Įkelta {len(full_df)} įrašų į duomenų bazę.")
