import pytest
import os
from ml_pipeline.classify_with_gpt_api import classify_with_api


# Skip test if API key is not set
@pytest.mark.skipif(os.getenv("OPENAI_API_KEY") is None, reason="OPENAI_API_KEY is not set")
@pytest.mark.parametrize("question", [
    "Dėl valstybės biudžeto projekto svarstymo",
    "Svarstomas klausimas dėl aplinkos oro kokybės gerinimo programos",
    "Informacija apie švietimo įstaigų finansavimą"
])
def test_classify_returns_valid_topic(question):
    result = classify_with_api(question)

    # Valid rezultatų patikra
    assert isinstance(result, str), "Grąžintas ne tekstas"
    assert result != "", "Grąžinta tuščia eilutė"
    assert result not in ["Vertimo klaida", "API užklausos klaida"], f"Klaida: {result}"
