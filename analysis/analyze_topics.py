import pandas as pd

def classify_topic(question):
    q = question.lower()
    if "region" in q:
        return "Regioninė politika"
    elif "komisijos" in q or "europos" in q or "es " in q or "com(" in q:
        return "Europos Sąjunga"
    elif "valdymo" in q or "strateginio" in q:
        return "Viešasis valdymas"
    elif "kultūr" in q:
        return "Kultūra"
    elif "vizij" in q:
        return "Strateginės gairės"
    else:
        return "Kita"

def generate_topic_summary(df):
    df = df[~df["question"].isin(exclude)].copy()
    df["topic"] = df["question"].apply(classify_topic)

    topic_counts = df["topic"].value_counts().reset_index()
    topic_counts.columns = ["Tema", "Klausimų skaičius"]

    print("\n📊 TEMŲ PASISKIRSTYMAS:\n")
    print(topic_counts)

    output_path = "data/agenda_items_with_topics.csv"
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"\n💾 Išsaugota: {output_path}")
    return df
