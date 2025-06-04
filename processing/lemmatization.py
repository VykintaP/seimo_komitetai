import stanza

stanza.download("lt", verbose=False)
nlp = stanza.Pipeline(lang="lt", processors="tokenize,lemma", use_gpu=False)



def lemmatize_text(text: str, stopwords: set) -> list[str]:

    if not text.strip():
        return []

    doc = nlp(text)
    lemmas = [word.lemma.lower() for sent in doc.sentences for word in sent.words]
    print(lemmas)
    return [lemma for lemma in lemmas if lemma not in stopwords and len(lemma) > 2]
