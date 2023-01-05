import pandas as pd
import requests  # type: ignore

from dishwashers.data import get_prediction_data, get_trainings_data
from dishwashers.process import DISHWASHER_REGISTRATION_PATH

DUMMY_DISHWASHER_REGISTRATION_PATH = "tests/test_data/dummy_dishwasher_registration.csv"
DUMMY_RECIPE_PAGE_PATH = "tests/test_data/dummy_recipe_page.txt"


def generate_dummy_dishwasher_registration() -> None:
    prediction_data = get_prediction_data(DISHWASHER_REGISTRATION_PATH)[:10]
    trainings_data = get_trainings_data(DISHWASHER_REGISTRATION_PATH)[:20]
    test_data = pd.concat([prediction_data, trainings_data])
    test_data.to_csv(DUMMY_DISHWASHER_REGISTRATION_PATH, index=False)


def generate_recipe_page() -> None:
    dummy_dishwasher_registration = pd.read_csv(DUMMY_DISHWASHER_REGISTRATION_PATH)
    url = dummy_dishwasher_registration["url"].iloc[0]
    response = requests.get(url=url)
    with open(DUMMY_RECIPE_PAGE_PATH, "w") as f:
        f.write(response.text)


if __name__ == "__main__":
    generate_dummy_dishwasher_registration()
    generate_recipe_page()
