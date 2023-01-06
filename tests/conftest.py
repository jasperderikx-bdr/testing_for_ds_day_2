import random
from pathlib import Path
from typing import Dict, Iterator

import pytest
from _pytest.monkeypatch import MonkeyPatch
from generate_test_data import DUMMY_DISHWASHER_REGISTRATION_PATH
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

import dishwashers.data
import dishwashers.model
from dishwashers.data import get_prediction_data, get_trainings_data
from dishwashers.model import DishwasherModel


@pytest.fixture(scope="session")
def monkey_session() -> Iterator[MonkeyPatch]:
    """This fixture is identical to monkeypatch, except it has a broader scope.

    This enables fixtures with a scope other than 'function', to make use of monkeypatch.
    """
    mp = MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(scope="module")
def restrict_grid_search(monkey_session: MonkeyPatch) -> None:
    class MockGridSearchCV(GridSearchCV):
        def __init__(self, pipeline: Pipeline, param_grid: Dict, cv: int) -> None:
            super().__init__(pipeline, param_grid={"RFR__max_depth": [2], "RFR__n_estimators": [5]}, cv=2)

    monkey_session.setattr(dishwashers.model, "GridSearchCV", MockGridSearchCV)


#  -- Exercise 6 --
# We've made sure scrape_duration_from_recipe_page() is tested for several scenarios in tests\test_data.py. To
# drastically reduce the runtime of the other tests, we want to monkeypatch it. The whole fixture is already written,
# al that is left is to complete the last line.
# Let the test in exercise 5 depend on this fixture and check with ```pytest --durations=-1 tests\test_model.py```
# how much time is gained.
@pytest.fixture(scope="module")
def mock_scraper(monkey_session: MonkeyPatch) -> None:
    random.seed(10)

    def mock_function(url: str) -> str:
        return f"{random.randint(10, 59)} min. bereiden"

    monkey_session.setattr(dishwashers.data, "scrape_duration_from_recipe_page", mock_function)


# This is how you should change the fixture and test of exercise 4 and 5.
@pytest.fixture(scope="module")
def trained_dishwasher_model_copy(restrict_grid_search: None, mock_scraper: None) -> Iterator[DishwasherModel]:
    dishwasher_model = DishwasherModel()
    trainings_data = get_trainings_data(file_path=Path(DUMMY_DISHWASHER_REGISTRATION_PATH))
    dishwasher_model.train(data=trainings_data)
    yield dishwasher_model


def test_predictions_are_positive_copy(trained_dishwasher_model_copy: DishwasherModel, mock_scraper: None) -> None:
    prediction_data = get_prediction_data(file_path=Path(DUMMY_DISHWASHER_REGISTRATION_PATH))
    predictions = trained_dishwasher_model_copy.predict(data=prediction_data)
    assert (predictions["prediction_dishwashers"] > 0).all()
