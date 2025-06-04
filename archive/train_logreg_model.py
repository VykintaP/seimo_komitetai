import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt
import joblib
from pathlib import Path

def train_model(data_path: str = "data/training_data.csv", model_dir: str = "model"):
    df = pd.read_csv(data_path)
    df = df[df["topic"].notnull()]

    vectorizer = TfidfVectorizer(ngram_range=(1, 2), max_features=5000)
    X = vectorizer.fit_transform(df["question"])
    y = df["topic"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)

    model = LogisticRegression(max_iter=1000, class_weight="balanced")
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    report = classification_report(y_test, y_pred, digits=3)
    print("== Klasifikavimo rezultatai ==")
    print(report)

    Path(model_dir).mkdir(parents=True, exist_ok=True)
    report_df = pd.DataFrame(classification_report(y_test, y_pred, output_dict=True)).transpose()
    report_df.to_csv(f"{model_dir}/classification_report.csv", float_format="%.3f")
    print(f"[INFO] Išsaugotas: {model_dir}/classification_report.csv")

    labels = sorted(df["topic"].unique())
    cm = confusion_matrix(y_test, y_pred, labels=labels)
    cm_df = pd.DataFrame(cm, index=labels, columns=labels)
    print("== Painiavos matrica (lentelė)==")
    print(cm_df)

    disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=labels)
    disp.plot(xticks_rotation=90)
    plt.tight_layout()
    plt.show()

    print("== Temų pasiskirstymas (mokymo rinkinyje) ==")
    print(y_train.value_counts(normalize=True).round(3))

    joblib.dump(model, f"{model_dir}/classifier.joblib")
    joblib.dump(vectorizer, f"{model_dir}/vectorizer.joblib")
    print(f"[INFO] Modelis išsaugotas: {model_dir}/classifier.joblib")
