from dotenv import load_dotenv
import os
import pytest
from classify_with_gpt_api import classify_with_api

@pytest.mark.parametrize("question", [
    "Svarstomas klausimas dėl aplinkos oro kokybės gerinimo programos",
    "Dėl valstybės biudžeto projekto svarstymo",
    "Informacija apie švietimo įstaigų finansavimą"
])
def test_classify_returns_valid_topic(question):
    result = classify_with_api(question)
    assert isinstance(result, str)
    assert result != "", "Grąžinta tuščia reikšmė"
    assert result != "Vertimo klaida", "Vertimo klaida"
    assert result != "API užklausos klaida", "API klaida"


load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if api_key:
    print("API raktas nuskaitytas sėkmingai.")
else:
    print("Nerastas API raktas.")
