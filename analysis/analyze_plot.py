import pandas as pd
from collections import Counter
import re
import matplotlib.pyplot as plt
from wordcloud import STOPWORDS

# 1. Įkeliame CSV
df = pd.read_csv("data/agenda_items.csv")

# 2. Atmetam neinformatyvius klausimus
exclude_questions = [
    "Posėdžio darbotvarkės tvirtinimas",
    "Kiti klausimai",
    "XVP-178"
]
df = df[~df["question"].isin(exclude_questions)]

# 3. Sujungiame į vieną tekstą
all_text = " ".join(df["question"].dropna().astype(str))
all_text = re.sub(r"[^\w\s]", "", all_text).lower()
words = all_text.split()

# 4. Stopwords
lt_stopwords = set([
    "ir", "dėl", "su", "bei", "už", "kiti", "klausimai",
    "posėdžio", "darbotvarkės", "tvirtinimas", "komiteto",
    "ateities", "sprendimo", "projekto", "klausimas",
    "apie", "kad", "ar", "tai", "jau", "kaip", "nuo", "iki", "per"
])
filtered_words = [w for w in words if w not in STOPWORDS and w not in lt_stopwords]

# 5. Skaičiuojam dažniausius
word_counts = Counter(filtered_words)
top_words = word_counts.most_common(20)
df_top = pd.DataFrame(top_words, columns=["Žodis", "Pasikartojimų skaičius"])

# 6. Braižom diagramą
plt.figure(figsize=(10, 6))
plt.bar(df_top["Žodis"], df_top["Pasikartojimų skaičius"], color="skyblue")
plt.title("Dažniausiai pasikartojantys žodžiai")
plt.xlabel("Žodis")
plt.ylabel("Pasikartojimų skaičius")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
