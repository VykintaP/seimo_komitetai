import pytest
import re
from pathlib import Path
from processing.scraper import get_committee_urls, CommitteeScraper

def test_committee_urls_are_retrieved_and_filtered():
    urls = get_committee_urls()
    assert len(urls) > 0, "Nerasta jokių komitetų"
    for name, _ in urls:
        assert "komisija" not in name.lower(), f"Komisija neturėtų būti įtraukta: {name}"

def test_agenda_links_for_known_committee():
    name = "Sveikatos reikalų komitetas"
    url = "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1"
    scraper = CommitteeScraper(name, url)
    links = scraper.fetch_agenda_links()
    assert isinstance(links, list), "Rezultatas turi būti sąrašas"
    assert len(links) > 0, "Nerasta jokių darbotvarkių"
    assert all("darbotvark" in link.lower() for link in links), "Yra netinkamų nuorodų"

def test_fetch_items_structure_from_one_agenda():
    name = "Sveikatos reikalų komitetas"
    agenda_url = "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1&p_event_id=41208"
    scraper = CommitteeScraper(name, "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1")
    items = scraper.fetch_items(agenda_url)
    assert isinstance(items, list), "fetch_items turi grąžinti sąrašą"
    if items:
        row = items[0]
        assert len(row) == 6, f"fetch_items turi grąžinti 6 laukus, gauta {len(row)}"
        assert re.match(r"\d{4}-\d{2}-\d{2}", row[0]), f"Neteisingas datos formatas: {row[0]}"
        assert isinstance(row[1], str) and len(row[1]) > 3, "Klausimo tekstas per trumpas arba tuščias"

def test_debug_html_creation(tmp_path):
    name = "Test Komitetas"
    scraper = CommitteeScraper(name, "https://www.lrs.lt/invalid-url")
    soup = scraper.get_soup()
    scraper.debug_html(soup)

    debug_path = Path("debug.html")
    assert debug_path.exists(), "debug.html nebuvo sukurtas"
    assert debug_path.read_text().startswith("<html") or "<!DOCTYPE html>" in debug_path.read_text()
    debug_path.unlink()  # ištrinti po testo

@pytest.mark.parametrize("name, url", get_committee_urls()[:3])
def test_fetch_items_structure_from_real_committees(name, url):
    scraper = CommitteeScraper(name, url)
    links = scraper.fetch_agenda_links()
    if links:
        items = scraper.fetch_items(links[0])
        assert isinstance(items, list), "fetch_items turi grąžinti sąrašą"
        if items:
            row = items[0]
            assert len(row) == 6, f"{name}: fetch_items turi grąžinti 6 laukus, gauta {len(row)}"
