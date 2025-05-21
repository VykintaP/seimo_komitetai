import pytest
from scraper.scraper import get_committee_urls, CommitteeScraper


def get_best_event_url(base_url):
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "lxml")
    links = soup.find_all("a", href=True)
    event_links = []
    for link in links:
        href = link["href"]
        if "p_event_id=" in href:
            full_url = "https://www.lrs.lt" + href if not href.startswith("http") else href
            event_links.append(full_url)
    if event_links:
        return event_links[1] if len(event_links) > 1 else event_links[0]
    return None


@pytest.mark.parametrize("name,url", get_committee_urls())
def test_event_of_each_committee(name, url):
    event_url = get_best_event_url(url)
    if not event_url:
        pytest.skip(f"{name} neturi nė vienos tinkamos darbotvarkės")
    scraper = CommitteeScraper(name, "")
    items = scraper.fetch_items(event_url)
    assert isinstance(items, list)
    assert len(items) > 0, f"{name} ({event_url}) grąžino 0 klausimų"
    for item in items:
        assert len(item) == 3
        assert isinstance(item[1], str)