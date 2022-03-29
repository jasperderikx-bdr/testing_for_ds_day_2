import pytest
from src.data.recipes import scrape_list_page, scrape_recipe_page
import validators


def test_scrape_list_page():
    urls = scrape_list_page(page=0)
    assert all(validators.url(url) for url in urls)


def test_scrape_recipe_page():
    result = scrape_recipe_page(
        url="https://www.ah.nl/allerhande/recept/R-R1196291/broodje-zalm-met-komkommer-radijs-en-mierikswortelcreme")
    assert result == "10 min. bereiden"
