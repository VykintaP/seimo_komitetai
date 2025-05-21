import pandas as pd
from collections import Counter
import re
from wordcloud import STOPWORDS


df = pd.read_csv("data/agenda_items.csv")


all_text = " ".join(df["question"].dropna().astype(str))

# 4. Pašalinam skyrybos ženklus, pavertžiam į mažąsias raides
all_text = re.sub(r"[^\w\s]", "", all_text).lower()

# 5. Suskaidom į žodžius
words = all_text.split()

# 6. Pašalinam stop žodžius (angliškus ir lietuviškus)
lt_stopwords = set([
    "ir", "dėl", "su", "bei", "už", "kiti", "klausimai",
    "posėdžio", "darbotvarkės", "tvirtinimas", "komiteto",
    "ateities", "sprendimo", "projekto", "klausimas",
    "apie", "kad", "ar", "tai", "jau", "kaip", "nuo", "iki", "per",
    "m", "metų", "metai", "planas", "plane", "valdymo", "darbai"
])
filtered_words = [w for w in words if w not in STOPWORDS and w not in lt_stopwords]

# 7. Skaičiuojam dažniausius žodžius
word_counts = Counter(filtered_words)
top_words = word_counts.most_common(20)

# 8. Paverčiam į lentelę ir atvaizduojam
df_top = pd.DataFrame(top_words, columns=["Žodis", "Pasikartojimų skaičius"])
print(df_top)


from classify import classify_topic

df["topic"] = df["question"].apply(classify_topic)

print(df[["date", "question", "topic"]].head(10))

