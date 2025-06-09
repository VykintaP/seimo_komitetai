import re
from pathlib import Path

import pytest

from processing.scraper import (
    CommitteeScraper,
    extract_project_id_from_text,
    get_committee_urls,
    run_scraper,
)


def test_run_scraper_creates_csv(tmp_path):
    """Tikrina ar scraper sugeneruoja CSV failus į nurodytą direktoriją"""
    run_scraper(output_dir=tmp_path)
    files = list(tmp_path.glob("*.csv"))
    assert len(files) > 0, "Nepavyko sugeneruoti jokių CSV"
    assert any("komitetas" in f.name or f.name.endswith(".csv") for f in files)


def test_committee_urls_are_retrieved_and_filtered():
    """Tikrina ar teisingai filtruojami komitetų URL adresai"""
    urls = get_committee_urls()
    assert len(urls) > 0, "Nerasta jokių komitetų"
    for name, _ in urls:
        assert (
                "komisija" not in name.lower()
        ), f"Komisija neturėtų būti įtraukta: {name}"


def test_agenda_links_for_known_committee():
    """Tikrina darbotvarkių URL gavimą iš komiteto puslapio"""
    name = "Ateities komitetas"
    url = "https://www.lrs.lt/sip/portal.show?p_r=38856"
    scraper = CommitteeScraper(name, url)
    links = scraper.fetch_agenda_links()
    assert isinstance(links, list), "Rezultatas turi būti sąrašas"
    assert len(links) > 0, "Nerasta jokių darbotvarkių"


def test_extract_project_id_variants():
    """Tikrina projekto numerio ištraukimą iš teksto"""
    assert extract_project_id_from_text("Projektas Nr. XIIIP-123") == "XIIIP-123"
    assert extract_project_id_from_text("Nr. ABC-456/789") == "ABC-456/789"
    assert extract_project_id_from_text("Tekstas be numerio") == ""


def test_fetch_items_handles_missing_fields():
    """Tikrina trūkstamų laukų apdorojimą darbotvarkėje"""
    url = "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1&p_event_id=41208"
    scraper = CommitteeScraper(
        "Sveikatos reikalų komitetas",
        "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1",
    )
    items = scraper.fetch_items(url)
    for row in items:
        assert len(row) == 6
        assert isinstance(row[1], str)  # klausimas


def test_fetch_items_structure_from_one_agenda():
    """Tikrina ištrauktų duomenų struktūrą iš vienos darbotvarkės"""
    name = "Sveikatos reikalų komitetas"
    agenda_url = "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1&p_event_id=41208"
    scraper = CommitteeScraper(
        name, "https://www.lrs.lt/sip/portal.show?p_r=35299&p_k=1"
    )
    items = scraper.fetch_items(agenda_url)
    assert isinstance(items, list), "fetch_items turi grąžinti sąrašą"
    if items:
        row = items[0]
        assert len(row) == 6, f"fetch_items turi grąžinti 6 laukus, gauta {len(row)}"
        assert re.match(
            r"\d{4}-\d{2}-\d{2}", row[0]
        ), f"Neteisingas datos formatas: {row[0]}"
        assert (
                isinstance(row[1], str) and len(row[1]) > 3
        ), "Klausimo tekstas per trumpas arba tuščias"


@pytest.mark.parametrize("name, url", get_committee_urls()[:3])
def test_fetch_items_structure_from_real_committees(name, url):
    """Tikrina duomenų struktūrą iš pirmų trijų komitetų"""
    scraper = CommitteeScraper(name, url)
    links = scraper.fetch_agenda_links()
    if links:
        items = scraper.fetch_items(links[0])
        assert isinstance(items, list), "fetch_items turi grąžinti sąrašą"
        if items:
            row = items[0]
            assert (
                    len(row) == 6
            ), f"{name}: fetch_items turi grąžinti 6 laukus, gauta {len(row)}"
