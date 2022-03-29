import requests
from bs4 import BeautifulSoup
from src.configuration import input_data_path
import pandas as pd


def scrape_recipe_page(url: str):
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        text = soup.find("div", class_="recipe-header-time_timeLine__nn84w").text
    except AttributeError:
        text = ""
    return text


def read_input_data():
    pd.read_csv(input_data_path)
