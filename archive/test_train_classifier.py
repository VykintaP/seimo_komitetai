import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
import tempfile
import joblib
import os

def test_train_model_pipeline():
    data = {
        "question": [
            "Kaip finansuojamos savivaldybės?",
            "Kaip paskirstomi biudžetai savivaldybėms?",
            "Kokie sprendimai dėl aplinkosaugos?",
            "Kaip mažinamas taršos lygis miestuose?",
            "Kaip veikia Europos Sąjungos fondai?",
            "Kokios yra ES paramos galimybės?"
        ],
        "topic": [
            "Ekonomika",
            "Ekonomika",
            "Aplinkosauga",
            "Aplinkosauga",
            "Europos Sąjunga",
            "Europos Sąjunga"
        ]
    }
    df = pd.DataFrame(data)
    vectorizer = TfidfVectorizer()
    X = vectorizer.fit_transform(df["question"])
    y = df["topic"]

    # Pakeista čia: test_size=0.5 vietoj default (0.25)
    X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, test_size=0.5, random_state=42)
    model = LogisticRegression(max_iter=1000)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    assert len(y_pred) == len(y_test)


def test_model_save(tmp_path):
    model = LogisticRegression()
    vectorizer = TfidfVectorizer()
    model_path = tmp_path / "model.joblib"
    vect_path = tmp_path / "vect.joblib"

    joblib.dump(model, model_path)
    joblib.dump(vectorizer, vect_path)

    assert model_path.exists()
    assert vect_path.exists()
