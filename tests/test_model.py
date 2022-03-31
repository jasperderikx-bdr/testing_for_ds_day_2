from pathlib import Path
from typing import Iterator

import pandas as pd
import pytest
from sklearn.pipeline import Pipeline

from dishwashers.data import get_prediction_data, get_trainings_data
from dishwashers.model import DishwasherModel


@pytest.fixture(scope="module")
def dishwasher_registration_path() -> Iterator[Path]:
    yield Path("tests/test_data/dummy_dishwasher_registration.csv")


@pytest.fixture(scope="module")
def trainings_data(dishwasher_registration_path: Path) -> Iterator[pd.DataFrame]:
    yield get_trainings_data(file_path=dishwasher_registration_path)


@pytest.fixture(scope="module")
def prediction_data(dishwasher_registration_path: Path) -> Iterator[pd.DataFrame]:
    yield get_prediction_data(file_path=dishwasher_registration_path)


@pytest.fixture(scope="module")
def trained_model(restrict_grid_search: None, trainings_data: pd.DataFrame, mock_scraper: None) -> Iterator[Pipeline]:
    model = DishwasherModel()
    model.train(data=trainings_data)
    yield model


def test_positive_predictions(trained_model: Pipeline, prediction_data: pd.DataFrame) -> None:
    predictions = trained_model.predict(prediction_data)
    assert all(predictions["prediction_dishwashers"] > 0)
