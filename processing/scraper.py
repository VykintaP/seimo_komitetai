import requests
from bs4 import BeautifulSoup
import pandas as pd
from pathlib import Path
import re
import logging
from unidecode import unidecode

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

def extract_project_id_from_text(text: str) -> str:
    matches = re.findall(
        r"(?:Projekt(?:o|as)?\s+Nr\.?|Įstatymo\s+projektas\s+Nr\.?|Dokumento\s+Nr\.?|Nr\.)\s*([A-Z0-9\-\/]+)",
        text, flags=re.IGNORECASE)
    return "; ".join(matches) if matches else ""

class CommitteeScraper:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    # Ieško <a> žymų, kur tekste yra „darbotvark“
    def fetch_agenda_links(self):
        response = requests.get(self.url)
        soup = BeautifulSoup(response.content, "lxml")
        links = soup.find_all("a")
        result = []
        for link in links:
            href = link.get("href")
            text = link.get_text(strip=True).lower()
            if "darbotvark" in text and href:
                full_url = href if href.startswith("http") else "https://www.lrs.lt" + href
                result.append(full_url)
        return result

    # ištraukia klausimus iš darbotvarkės lentelės
    def fetch_items(self, agenda_url):
        response = requests.get(agenda_url)
        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find("table", class_="darb")
        rows = table.find_all("tr") if table else []
        if not rows:
            return []

        header_cells = rows[0].find_all("td") or rows[0].find_all("th")
        header_map = {i: cell.get_text(strip=True).lower() for i, cell in enumerate(header_cells)}

        # Nustato indeksus pagal raktinius žodžius
        date_idx = next((i for i, t in header_map.items() if "dat" in t or "laik" in t), None)
        question_idx = next((i for i, t in header_map.items() if "klausim" in t), None)
        project_idx = next((i for i, t in header_map.items() if "projekto" in t or "projekt" in t or "dokument" in t),
                           None)
        responsible_idx = next((i for i, t in header_map.items() if "rengėj" in t or "atsaking" in t), None)
        invited_idx = next((i for i, t in header_map.items() if "kviečiam" in t or "pranešėj" in t), None)

        if date_idx is None or question_idx is None:
            logging.warning("Nepavyko nustatyti date/question stulpelių – praleidžiama")
            return []

        items = []
        current_invited_block = []
        current_question = None
        current_date = ""
        current_project = ""
        current_responsible = ""

        for row in rows[1:]:
            cells = row.find_all("td")
            if max(date_idx, question_idx) >= len(cells):
                continue

            raw_date = cells[date_idx].get_text(strip=True)
            date_match = re.search(r"\d{4}-\d{2}-\d{2}", raw_date)
            if date_match:
                current_date = pd.to_datetime(date_match.group()).strftime("%Y-%m-%d")

            raw_text = cells[question_idx].get_text(separator=" ", strip=True)
            if len(raw_text) >= 5 and not re.match(r"^\d+(\.\d+)?$", raw_text):
                project_from_text = extract_project_id_from_text(raw_text)
                cell_project_text = cells[project_idx].get_text(
                    strip=True) if project_idx is not None and project_idx < len(cells) else ""
                current_project = project_from_text or cell_project_text
                current_responsible = cells[responsible_idx].get_text(
                    strip=True) if responsible_idx is not None and responsible_idx < len(cells) else ""
                invited = "; ".join(current_invited_block)
                items.append((
                    current_date,
                    raw_text,
                    self.name,
                    current_project,
                    current_responsible,
                    invited
                ))
                current_invited_block = []


        return items

# Surenka visas nuorodas
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
        urls.append((title, full_url))
    return urls

def run_scraper(output_dir=None):
    if output_dir is None:
        output_dir = Path(__file__).resolve().parents[1] / "data" / "raw"

    committee_urls = get_committee_urls()
    logging.info(f"Rasta {len(committee_urls)} komitetų")

    raw_dir = output_dir
    raw_dir.mkdir(parents=True, exist_ok=True)

    # surenka darbotvarkes
    for name, url in committee_urls:
        try:
            scraper = CommitteeScraper(name, url)
            agenda_links = scraper.fetch_agenda_links()
            logging.info(f"{name}: {len(agenda_links)} darbotvarkių")

            all_items = []
            for agenda_url in agenda_links:
                try:
                    items = scraper.fetch_items(agenda_url)
                    all_items.extend(items)
                    logging.info(f"  {len(items)} klausimų iš {agenda_url}")
                except Exception as e:
                    logging.warning(f"  Klaida analizuojant {agenda_url}: {e}")

            # sukuria lenteles
            df = pd.DataFrame(all_items, columns=["date", "question", "committee", "project", "responsible", "attendees"])
            filename = unidecode(name.lower()).replace(" ", "_").replace("-", "_")
            filepath = raw_dir / f"{filename}.csv"
            df.to_csv(filepath, index=False, encoding="utf-8")
            logging.info(f"  Išsaugota {len(df)} klausimų į {filepath}")

        except Exception as e:
            logging.error(f"Klaida komiteto puslapyje {url}: {e}")
        raw_dir = output_dir
if __name__ == "__main__":
    run_scraper()
