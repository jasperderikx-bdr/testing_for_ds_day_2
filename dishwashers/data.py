from __future__ import annotations

import re
from pathlib import Path

import pandas as pd
import requests  # type: ignore
from bs4 import BeautifulSoup
from sklearn.base import BaseEstimator, TransformerMixin


def scrape_duration_from_recipe_page(url: str) -> str:
    response = requests.get(url=url)
    soup = BeautifulSoup(response.content, "html.parser")
    try:
        duration = soup.find("div", class_="recipe-header-time_timeLine__nn84w").text
    except AttributeError:
        duration = ""
    return duration


def retrieve_first_number(text: str, pattern: str) -> int:
    subtext = re.search(pattern=pattern, string=text)
    if subtext is None:
        return 0
    else:
        number = re.search("[0-9]+", subtext.group())
        if number is None:
            return 0
        else:
            return int(number.group())


def parse_duration(text: str) -> int:
    """Converts string that contains duration to number of minutes. Typical example: '1 uur 30 min. bereiden' -> 90."""
    minutes = retrieve_first_number(text, "[0-9]+ min.")
    hours = retrieve_first_number(text, "[0-9]+ uur")
    return hours * 60 + minutes


class AddRecipeDuration(BaseEstimator, TransformerMixin):
    """Transformer to add duration of recipe in minutes as column."""

    def fit(self, x: pd.DataFrame, y: pd.Series) -> AddRecipeDuration:
        return self

    @staticmethod
    def transform(x: pd.DataFrame) -> pd.DataFrame:
        x_ = x.copy()
        x_["duration"] = x_["url"].apply(scrape_duration_from_recipe_page)
        x_["duration_minutes"] = x_.duration.apply(parse_duration)
        return x_[["colleagues", "duration_minutes"]]


def get_trainings_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = df.dropna(subset=["dishwashers"])  # Remove rows without label.
    return df


def get_prediction_data(file_path: Path) -> pd.DataFrame:
    df = pd.read_csv(file_path)
    df = df[df["dishwashers"].isna()]  # Keep only rows without label.
    return df
