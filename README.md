# Seimo temų filtratorius

Teminis klasifikatorius Lietuvos Respublikos Seimo komitetų darbotvarkėms

## Apie projektą

Šis projektas automatizuoja Lietuvos Respublikos Seimo komitetų darbotvarkių turinio apdorojimą. Sistema surenka darbotvarkių duomenis iš oficialaus Seimo puslapio, išvalo nereikalingą tekstą, suklasifikuoja kiekvieną klausimą pagal iš anksto apibrėžtas viešosios politikos temas ir pateikia interaktyvią analizę. Klasifikavimui naudojamas didelės apimties kalbos modelis Mistral-7B-Instruct-v0.1, veikiantis zero-shot principu, be išankstinio modelio apmokymo konkrečiomis temomis. Klasifikavimo temos atitinka Lietuvos Respublikos Vyriausybės strategines kryptis.

## Diegimas

1. Sukurkite virtualią Python aplinką (pvz., venv):

    python -m venv .venv
    source .venv/bin/activate

    Windows naudotojams:

    .venv\Scripts\activate

2. Įdiekite reikalingus paketus:

    pip install -r requirements.txt

3. Prisijunkite prie Hugging Face paskyros:

    huggingface-cli login

4. Paprašykite prieigos prie Mistral modelio:

    https://huggingface.co/mistralai/Mistral-7B-Instruct-v0.1

## Paleidimas

Norint įvykdyti visą automatizuotą procesą (nuo duomenų surinkimo iki klasifikavimo ir treniravimo):

    python scripts/run_pipeline.py

Norint atidaryti interaktyvų vizualizacijos puslapį:

    python visualize/dashboard.py

## Aplankų struktūra

- data/raw – pradiniai CSV failai, surinkti iš Seimo svetainės
- data/cleaned – išvalyti klausimai po valymo žingsnio
- data/classified – suklasifikuoti klausimai su priskirta tema
- data/diagnostics – duomenų kokybės analizės rezultatai

## Temos

Klasifikavimui naudojamos temos atitinka Vyriausybės strateginių krypčių politikos sritis: valstybės valdymas, aplinka, energetika, finansai, sveikata, švietimas, teisingumas ir kt.

## Testavimas

Norėdami paleisti automatinį testų rinkinį:

    python scripts/run_tests.py

## Autorius

Projektą sukūrė Vykinta P. kaip tarpdisciplininį duomenų analizės, NLP ir viešosios politikos tyrimų įrankį.
