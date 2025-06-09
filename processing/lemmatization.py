import stanza

# Parsisiunčia lietuvių kalbos modelį  
stanza.download("lt", verbose=False)

# Inicializuoja stanza pipeline'ą su lietuvių kalbos tokenizacijos ir lematizacijos procesoriais
nlp = stanza.Pipeline(lang="lt", processors="tokenize,lemma", use_gpu=False)


def lemmatize_text(text: str, stopwords: set) -> list[str]:
    """Lematizuoja tekstą ir pašalina stop žodžius bei trumpus žodžius."""

    # Grąžina tuščią sąrašą, jei tekstas tuščias
    if not text.strip():
        return []

    doc = nlp(text)
    lemmas = [word.lemma.lower() for sent in doc.sentences for word in sent.words]
    print(lemmas)  # Debug tikslais
    return [lemma for lemma in lemmas if lemma not in stopwords and len(lemma) > 2]
