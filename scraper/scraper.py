import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from pathlib import Path
from unidecode import unidecode

def fetch_committee_name(soup):
    div = soup.find("div", class_="wide-title color-light")
    return div.get_text(strip=True) if div else "Unknown committee"

def fetch_agenda_links(soup, committee):
    links = soup.find_all("a")
    result = []
    for link in links:
        href = link.get("href")
        text = link.get_text(strip=True).lower()
        if "darbotvark" in text and href:
            full_url = href if href.startswith("http") else "https://www.lrs.lt" + href
            result.append((full_url, committee))
    return result

def clean_question(text: str) -> str:
    text = re.sub(r"Įstatymo\s+Nr\.[^\s,]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"projekt[ao]?\s+Nr\.[^\s,]*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"Nr\.[^\s,]*", "", text)
    # Tik jei skliaustuose nėra žodžio „uždaras“, juos pašalinam
    if "uždaras" not in text.lower():
        text = re.sub(r"\([^)]*\)", "", text)
    text = re.sub(r"\s{2,}", " ", text)
    return text.strip().rstrip(",.:")

def fetch_agenda_items(url, committee):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "lxml")
    table = soup.find("table", class_="darb")
    rows = table.find_all("tr") if table else []
    if not rows:
        return []

    header_cells = rows[0].find_all("td") or rows[0].find_all("th")
    header_map = {i: cell.get_text(strip=True).lower() for i, cell in enumerate(header_cells)}

    date_idx, question_idx = None, None
    for idx, text in header_map.items():
        if "data" in text and "vieta" in text:
            date_idx = idx
        elif "klausimas" in text:
            question_idx = idx

    if date_idx is None or question_idx is None:
        for i, cell in enumerate(header_cells):
            cell_text = cell.get_text(strip=True).lower()
            if date_idx is None and "data" in cell_text:
                date_idx = i
            if question_idx is None and "klausim" in cell_text:
                question_idx = i
        if date_idx is None:
            date_idx = 1 if len(header_cells) > 1 else 0
        if question_idx is None:
            question_idx = 2 if len(header_cells) > 2 else 1

    items = []

    for row in rows[1:]:
        cells = row.find_all("td")
        if max(date_idx, question_idx) >= len(cells):
            continue

        raw_date = cells[date_idx].get_text(strip=True)
        date_match = re.search(r"\d{4}-\d{2}-\d{2}", raw_date)
        if not date_match:
            continue
        date = pd.to_datetime(date_match.group()).strftime("%Y-%m-%d")

        raw_text = cells[question_idx].get_text(separator=" ", strip=True)
        line = raw_text.strip()

        if line and not any(kw in line.lower() for kw in ["kviečiami", "pranešėjai", "pirmininkas"]):
            if not re.match(r"^[A-ZĮŲŽŠČĖ][a-ząčęėįšųūž]+\s+[A-ZĮŲŽŠČĖ]", line):
                cleaned_question = clean_question(line)
                if cleaned_question and len(cleaned_question.split()) >= 2:
                    items.append((date, cleaned_question, committee))

    return items

def get_committee_urls():
    base_url = "https://www.lrs.lt/sip/portal.show?p_r=35733"
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "lxml")
    links = soup.select("a.link.color-primary")
    urls = []
    for link in links:
        href = link.get("href")
        title = link.get_text(strip=True)
        if "komisija" in title.lower():
            continue
        full_url = href if href.startswith("http") else "https://www.lrs.lt" + href
        urls.append(full_url)
    return urls

def run_scraper():
    committee_urls = get_committee_urls()
    print(f"Rasta {len(committee_urls)} komitetų")
    data_dir = Path(__file__).resolve().parents[1] / "data"
    data_dir.mkdir(parents=True, exist_ok=True)

    for url in committee_urls:
        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.content, "lxml")
            committee = fetch_committee_name(soup)
            print(f"\nProcessing: {committee}")
            agenda_links = fetch_agenda_links(soup, committee)
            print(f"  Rasta darbotvarkių: {len(agenda_links)}")

            committee_items = []
            for agenda_url, _ in agenda_links:
                try:
                    items = fetch_agenda_items(agenda_url, committee)
                    committee_items.extend(items)
                    print(f"    {len(items)} klausimų iš {agenda_url}")
                except Exception as e:
                    print(f"    Klaida analizuojant {agenda_url}: {e}")

            if committee_items:
                df = pd.DataFrame(committee_items, columns=["date", "question", "committee"])
                filename = unidecode(committee.lower()).replace(" ", "_").replace("-", "_")
                filepath = data_dir / f"{filename}.csv"
                df.to_csv(filepath, index=False, encoding="utf-8")
                print(f"  Išsaugota {len(df)} eilučių į {filepath}")
            else:
                print(f"  Nepavyko surinkti klausimų – praleidžiama")

        except Exception as e:
            print(f"Klaida komiteto puslapyje {url}: {e}")

if __name__ == "__main__":
    run_scraper()
