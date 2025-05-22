import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from pathlib import Path
from unidecode import unidecode
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

class CommitteeScraper:
    def __init__(self, name, url):
        self.name = name
        self.url = url

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

    def fetch_items(self, agenda_url):
        response = requests.get(agenda_url)
        soup = BeautifulSoup(response.content, "lxml")
        table = soup.find("table", class_="darb")
        rows = table.find_all("tr") if table else []
        if not rows:
            return []

        header_cells = rows[0].find_all("td") or rows[0].find_all("th")
        header_map = {i: cell.get_text(strip=True).lower() for i, cell in enumerate(header_cells)}
        logging.debug(f"Header map: {header_map}")
        logging.warning(f"Darbotvarkės URL: {agenda_url}")
        logging.warning(f"Pirmos eilutės langeliai: {[c.get_text(strip=True) for c in header_cells]}")

        date_idx = next((i for i, t in header_map.items() if "data" in t or "laikas" in t), None)
        question_idx = next((i for i, t in header_map.items() if "klausim" in t), None)
        project_idx = next(
            (i for i, t in header_map.items() if "projekto nr" in t or "projekto" in t or "dokument" in t), None)
        responsible_idx = next((i for i, t in header_map.items() if "rengėjas" in t or "atsakingas" in t), None)
        invited_idx = next((i for i, t in header_map.items() if "kviečiami" in t or "pranešėj" in t), None)

        if date_idx is None or question_idx is None:
            logging.warning("Nepavyko nustatyti date/question stulpelių – praleidžiama lentelė")
            return []

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

            raw_text = cells[question_idx].get_text(separator="\n", strip=True)
            lines = raw_text.splitlines()
            for line in lines:
                line = line.strip()
                if not line or len(line.split()) < 2:
                    continue

                project = cells[project_idx].get_text(strip=True) if project_idx is not None and project_idx < len(cells) else ""
                responsible = cells[responsible_idx].get_text(strip=True) if responsible_idx is not None and responsible_idx < len(cells) else ""
                invited = cells[invited_idx].get_text(strip=True) if invited_idx is not None and invited_idx < len(cells) else ""


                items.append((date, line, self.name, project, responsible, invited))

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
        urls.append((title, full_url))
    return urls

def run_scraper():
    committee_urls = get_committee_urls()
    logging.info(f"Rasta {len(committee_urls)} komitetų")
    raw_dir = Path(__file__).resolve().parents[1] / "data" / "raw"
    raw_dir.mkdir(parents=True, exist_ok=True)

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

            if all_items:
                df = pd.DataFrame(all_items, columns=["date", "question", "committee", "project_id", "responsible_actor", "invited_presenters"])
                filename = unidecode(name.lower()).replace(" ", "_").replace("-", "_")
                filepath = raw_dir / f"{filename}.csv"
                df.to_csv(filepath, index=False, encoding="utf-8")
                logging.info(f"  Išsaugota {len(df)} klausimų į {filepath}")
            else:
                logging.warning(f"  {name}: Nepavyko surinkti klausimų")

        except Exception as e:
            logging.error(f"Klaida komiteto puslapyje {url}: {e}")

if __name__ == "__main__":
    run_scraper()
