import pandas as pd
import requests
from bs4 import BeautifulSoup
from src.data import scrape_recipe_page
import pandas as pd
import numpy as np
from datetime import date, timedelta
import math
import re


def get_fridays(length: int):
    days = [date(2020, 1, 1) + timedelta(days=d) for d in range(365 * 2)]
    fridays = [d for d in days if d.weekday() == 4]
    return fridays[:length]


FILE_PATH_RECIPE_LIST_PAGE = "tests/test_data/webpages/recipe_list_page.txt"
FILE_PATH_RECIPE_PAGE = "tests/test_data/webpages/recipe_page.txt"


def list_page_url(page=0):
    return f"https://www.ah.nl/allerhande/recepten-zoeken?menugang=lunch&page={page}"


def scrape_list_page(page: int):
    response = requests.get(list_page_url(page=page))
    soup = BeautifulSoup(response.content, "html.parser")
    results = soup.find(id="app")
    recipe_boxes = results.find_all("div", class_="column xxlarge-4 large-6 small-12")
    recipe_urls = [x.find("a") for x in recipe_boxes]
    recipe_urls = ["https://www.ah.nl" + x["href"] for x in recipe_urls if x is not None]
    return recipe_urls


def generate_input_data():
    recipe_urls = [scrape_list_page(page=i) for i in range(25)]
    recipe_urls = [x for l in recipe_urls for x in l]
    df = pd.DataFrame(recipe_urls, columns=["url"])
    df["duration"] = df.url.apply(scrape_recipe_page)
    # df["date"] = get_fridays(length=df.shape[0])
    # df["colleagues"] = np.random.randint(5, 35, df.shape[0])
    # df["duration_minutes"] = df.duration.apply(lambda x: int(re.search('[0-9]+', x).group()))
    # df["dishwashers"] = df["colleagues"] * df["duration_minutes"] / 100 + np.random.randint(0, 2, df.shape[0])
    # df["dishwashers"] = df["dishwashers"].apply(math.ceil)
    # df = df[["date", "url", "colleagues", "dishwashers", "duration_minutes", "duration"]]
    df.to_csv("tests/test_data/input_data.csv", index=False)


def save_webpage(url: str, file_path: str) -> None:
    response = requests.get(url=url)
    with open(file_path, "w") as f:
        f.write(response.text)


def read_webpage_from_txt(file_path: str) -> BeautifulSoup:
    with open(file_path) as f:
        return BeautifulSoup("".join(f.readlines()), "html.parser")


def generate_recipe_list_page():
    save_webpage(url=list_page_url(page=0),
                 file_path=FILE_PATH_RECIPE_LIST_PAGE)


def generate_recipe_page():
    urls = scrape_list_page(page=0)
    url = urls[0]
    save_webpage(url=url, file_path=FILE_PATH_RECIPE_PAGE)


if __name__ == "__main__":
    # generate_recipe_list_page()
    # generate_recipe_page()
    generate_input_data()
