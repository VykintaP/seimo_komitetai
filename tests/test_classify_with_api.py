import os

import pytest

from ml_pipeline.classify_with_gpt_api import classify_with_api

"""Testavimo byla API klasifikatoriaus funkcionalumui"""


# Praleisti testą jei nenustatytas API raktas
@pytest.mark.skipif(
    os.getenv("OPENAI_API_KEY") is None, reason="OPENAI_API_KEY is not set"
)
@pytest.mark.parametrize(
    "question",
    [
        "Dėl valstybės biudžeto projekto svarstymo",
        "Svarstomas klausimas dėl aplinkos oro kokybės gerinimo programos",
        "Informacija apie švietimo įstaigų finansavimą",
    ],
)
def test_classify_returns_valid_topic(question):
    """Tikrina ar klasifikatorius grąžina validžią temą"""
    result = classify_with_api(question)

    # Tikriname ar grąžintas rezultatas atitinka reikalavimus
    assert isinstance(result, str), "Grąžintas ne tekstas"
    assert result != "", "Grąžinta tuščia eilutė"
    assert result not in ["Vertimo klaida", "API užklausos klaida"], f"Klaida: {result}"
