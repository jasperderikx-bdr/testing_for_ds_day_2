from random import randint
from typing import Dict, Iterator

import pytest
from _pytest.monkeypatch import MonkeyPatch
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline

import dishwashers.data
import dishwashers.model


@pytest.fixture(scope="session")
def monkey_session() -> Iterator[MonkeyPatch]:
    mp = MonkeyPatch()
    yield mp
    mp.undo()


@pytest.fixture(scope="module")
def restrict_grid_search(monkey_session: MonkeyPatch) -> None:
    class MockGridSearchCV(GridSearchCV):
        def __init__(self, pipeline: Pipeline, param_grid: Dict, cv: int) -> None:
            super().__init__(pipeline, param_grid={"RFR__max_depth": [2], "RFR__n_estimators": [5]}, cv=2)

    monkey_session.setattr(dishwashers.model, "GridSearchCV", MockGridSearchCV)


@pytest.fixture(scope="module")
def mock_scraper(monkey_session: MonkeyPatch) -> None:
    def mock_function(url: str) -> str:
        return f"{randint(10, 59)} min. bereiden"

    monkey_session.setattr(dishwashers.data, "scrape_duration_from_recipe_page", mock_function)
