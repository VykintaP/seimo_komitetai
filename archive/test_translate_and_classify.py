import pandas as pd

from archive.zero_shot import classify_dataframe, classify_question


def test_classify_question_returns_valid_output():
    question = "Kaip bus reformuojamas sveikatos sektorius?"
    topic, score, translated = classify_question(question)
    assert isinstance(topic, str)
    assert isinstance(score, float)
    assert isinstance(translated, str)
    assert 0.0 <= score <= 1.0
    assert len(topic) > 1


def test_classify_dataframe_structure():
    df = pd.DataFrame({"question": ["Kokie pokyčiai švietimo srityje?"]})
    result_df = classify_dataframe(df)
    assert "predicted_topic_lt" in result_df.columns
    assert "confidence_score" in result_df.columns
    assert "translated_question" in result_df.columns
    assert not result_df.empty
