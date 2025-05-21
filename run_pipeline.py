from processing.merge_agendas import merge_agendas
from processing.clean_questions import clean_questions
from processing.classify import classify_agenda_items
from pathlib import Path

def run_pipeline():
    print("1. Merginami komitetų CSV failai...")
    merged_df = merge_agendas()
    if merged_df.empty:
        print("Nerasta komitetų failų. Vykdymas stabdomas.")
        return

    print(f"Rasta {len(merged_df)} įrašų.")

    print("2. Valomi klausimai...")
    cleaned_df = clean_questions()
    print(f"Po valymo liko {len(cleaned_df)} klausimų.")

    print("3. Priskiriamos temos...")
    classified_df = classify_agenda_items(cleaned_df)

    output_path = Path("data/agenda_items_with_topics.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    classified_df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Išsaugota: {output_path} ({len(classified_df)} įrašų)")

if __name__ == "__main__":
    run_pipeline()
