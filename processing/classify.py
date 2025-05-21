def classify_topic(question, committee=None):
    q = question.lower()

    if any(kw in q for kw in ["region", "savivaldyb", "apskri", "vietos bendruomen", "kraštovaizd", "teritorij"]):
        return "Regioninė politika"

    if any(kw in q for kw in ["kultūr", "paveld", "muziej", "knyg", "kūryb", "menų", "teatr"]):
        return "Kultūra"

    if any(kw in q for kw in ["valdymo", "valstybės tarnyb", "strategin", "reform", "efektyvum", "administrav", "planavim"]):
        return "Valdymas"

    if any(kw in q for kw in ["ekonomik", "finans", "mokesč", "biudžet", "investic", "pajam", "pvm", "akciz"]):
        return "Ekonomika"

    if any(kw in q for kw in ["europ", "es ", "europos komisij", "ekom", "eu", "tarptautin"]):
        return "Europos Sąjunga"

    if any(kw in q for kw in ["sveikat", "gydy", "ligon", "psichikos", "vaist", "pacient", "sveikatos apsaug"]):
        return "Sveikata"

    if any(kw in q for kw in ["švietim", "mokykl", "ugdym", "student", "mokym", "universitet", "edukacij", "mokslo"]):
        return "Švietimas"

    if any(kw in q for kw in ["socialin", "darbo rinka", "pašalp", "negal", "bedarb", "užimtum", "senatv", "pensij"]):
        return "Socialinė politika"

    if any(kw in q for kw in ["aplink", "tarša", "klimat", "atliek", "mišk", "gamta", "biologinė įvairov"]):
        return "Aplinkosauga"

    if any(kw in q for kw in ["gynyb", "saugum", "kariuomen", "karinė", "nacionalin", "grėsm", "krizė", "ekstremali situacija", "civilinė sauga"]):
        return "Saugumas"

    if any(kw in q for kw in ["pandemij", "evakuacij", "pasirengimas krizei", "rizik", "valstybės rezervo"]):
        return "Krizės valdymas"

    if any(kw in q for kw in ["vertyb", "šeima", "moral", "istorij", "atmint", "paveldo apsauga"]):
        return "Ideologiniai klausimai"

    if committee:
        c = committee.lower()
        if "kultūros" in c:
            return "Kultūra"
        if "sveikatos" in c:
            return "Sveikata"
        if "švietimo" in c:
            return "Švietimas"
        if "socialinių" in c:
            return "Socialinė politika"
        if "aplinkos" in c:
            return "Aplinkosauga"
        if "gynybos" in c or "saugumo" in c:
            return "Saugumas"
        if "biudžeto" in c or "finansų" in c:
            return "Ekonomika"

    return "Mišrūs / įvairūs klausimai"

def classify_agenda_items(df):
    df["topic"] = df.apply(lambda row: classify_topic(row["question"], row.get("committee")), axis=1)
    return df