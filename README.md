# Seimo temų filtratorius

**Teminis klasifikatorius Lietuvos Respublikos Seimo komitetų darbotvarkėms**

---

## 🔍 Apie projektą

Šis projektas automatizuoja Lietuvos Respublikos Seimo komitetų darbotvarkių turinio apdorojimą.
Sistema surenka darbotvarkių duomenis iš oficialaus Seimo puslapio, išvalo nereikalingą tekstą,
suklasifikuoja kiekvieną klausimą pagal iš anksto apibrėžtas viešosios politikos temas ir pateikia
interaktyvią analizę.

* Klasifikavimui naudojamas **OpenAI kalbos modelis** (zero-shot principu), be išankstinio specialaus mokymo konkrečiomis temomis.
* Temos atitinka Lietuvos Respublikos Vyriausybės strategines kryptis.

---

## 🚀 Live demo

📌 **Peržiūrėkite interaktyvų dashboard online:**
👉 [https://seimo-komitetai.onrender.com/](https://seimo-komitetai.onrender.com/)

---

## ⚙️ Diegimas

Sukurkite virtualią Python aplinką (pvz., venv):

```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows naudotojams:**

```
.venv\Scripts\activate
```

Įdiekite reikalingus paketus:

```
pip install -r requirements.txt
```

Prisijunkite prie OpenAI paskyros (API key):

```
export OPENAI_API_KEY="YOUR_KEY_HERE"
```

arba Windows:

```
set OPENAI_API_KEY="YOUR_KEY_HERE"
```

---

## 🚀 Paleidimas

Norint įvykdyti visą automatizuotą procesą (nuo duomenų surinkimo iki klasifikavimo):

```
python scripts/run_pipeline.py
```

Norint atidaryti interaktyvų vizualizacijos puslapį lokaliai:

```
python visualize/dashboard.py
```

---

## 📂 Aplankų struktūra

* `data/raw` – pradiniai CSV failai, surinkti iš Seimo svetainės
* `data/cleaned` – išvalyti klausimai po teksto apdorojimo
* `data/classified` – suklasifikuoti klausimai su priskirta tema
* `data/diagnostics` – duomenų kokybės analizės rezultatai

---

## 🏷 Temos

Klasifikavimui naudojamos temos atitinka Vyriausybės strateginių krypčių politikos sritis:
valstybės valdymas, aplinka, energetika, finansai, sveikata, švietimas, teisingumas ir kt.

---

## ✅ Testavimas

Norėdami paleisti automatinį testų rinkinį:

```
python scripts/run_tests.py
```

---

## 👩‍💻 Autorius

Projektą sukūrė **Vykinta P.** kaip tarpdisciplininį duomenų analizės, NLP ir viešosios politikos tyrimų įrankį.
