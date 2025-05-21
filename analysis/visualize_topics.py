import matplotlib.pyplot as plt
import seaborn as sns

# Pasiruošiam duomenis
df["date"] = pd.to_datetime(df["date"])
df["month"] = df["date"].dt.to_period("M").astype(str)

topic_counts = df.groupby(["month", "topic"]).size().reset_index(name="count")

# Braižom
plt.figure(figsize=(12, 6))
sns.lineplot(data=topic_counts, x="month", y="count", hue="topic", marker="o")

plt.title("Temų pasikartojimas Ateities komitete per laiką")
plt.xlabel("Mėnuo")
plt.ylabel("Klausimų skaičius")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()
