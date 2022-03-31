import pytest
import requests  # type: ignore
from _pytest.monkeypatch import MonkeyPatch

from dishwashers.data import parse_duration, scrape_duration_from_recipe_page
from tests.generate_test_data import DUMMY_RECIPE_PAGE_PATH


def test_scrape_duration_from_recipe_page(monkeypatch: MonkeyPatch) -> None:
    class MockRequestsGet:
        def __init__(self, url: str):
            with open(DUMMY_RECIPE_PAGE_PATH) as f:
                self.content = "".join(f.readlines())

    monkeypatch.setattr(requests, "get", MockRequestsGet)
    duration = scrape_duration_from_recipe_page(url="")
    assert duration == "20 min. bereiden"


def test_scrape_duration_from_recipe_page_bad_page(monkeypatch: MonkeyPatch) -> None:
    class MockRequestsGet:
        def __init__(self, url: str):
            self.content = "<bad html>"

    monkeypatch.setattr(requests, "get", MockRequestsGet)
    duration = scrape_duration_from_recipe_page(url="")
    assert duration == ""


@pytest.mark.parametrize("text, expected",
                         [("2 uur", 120),
                          ("30 min. bereiden", 30),
                          ("1 uur 30 min. bereiden", 90)])
def test_parse_duration(text: str, expected: int) -> None:
    assert parse_duration(text) == expected
