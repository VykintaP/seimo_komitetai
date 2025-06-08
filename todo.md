# TO DO – Seimo temų filtratorius (7 dienų sprintas)

## 1 diena – Duomenų bazė ir duomenų paruošimas
- [ ] Paleisti `run_pipeline.py` ir įsitikinti, kad sukuria `classified_questions.db`
- [ ] Patikrinti ar DB turi: `komitetas`, `tema`, `klausimas`, `data`
- [ ] Sukurti `dashboard.py`, kuris prisijungia prie DB ir `print()` išveda lentelę

## 2 diena – Vizualizacija: temos pagal komitetą
- [ ] Dropdown su komitetų sąrašu
- [ ] Filtruoti duomenis pagal pasirinktą komitetą
- [ ] Bar chart su temų skaičiumi (`plotly.express.bar`)

## 3 diena – Klausimų sąrašas
- [ ] Paimti `clickData` iš baro grafiko
- [ ] DataTable su klausimų sąrašu (filtruota pagal komitetą ir temą)

## 4 diena – Laiko filtras
- [ ] Įtraukti DatePickerRange arba RangeSlider
- [ ] Pritaikyti filtravimą visiems komponentams

## 5 diena – UI struktūra ir CSS
- [ ] Įrašyti antraštę (html.H1)
- [ ] Struktūruoti puslapį: filtrai | grafikas | lentelė
- [ ] Sukurti `assets/custom.css` su baziniu dizainu

## 6 diena – Stabilumas ir edge-case'ai
- [ ] „No data“ pranešimas kai nėra rezultatų
- [ ] Error handling (NoneType, tušti DataFrame ir pan.)
- [ ] Debug print() arba logger.info pagrindinėse vietose

## 7 diena – Dokumentacija ir demonstracija
- [ ] Parašyti README.md: kaip paleisti, ką reikia turėti
- [ ] Sukurti bent vieną screenshot arba trumpą video
- [ ] Patikrinti pilną paleidimą: `run_pipeline.py` + `dashboard.py`
