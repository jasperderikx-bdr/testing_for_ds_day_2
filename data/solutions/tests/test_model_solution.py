from pathlib import Path
from typing import Iterator

import pytest
from generate_test_data import DUMMY_DISHWASHER_REGISTRATION_PATH

from dishwashers.data import get_prediction_data, get_trainings_data
from dishwashers.model import DishwasherModel


# -- Exercise 4 --
# Write a module scoped fixture that yields an instance of DishwasherModel, trained on the labelled data in
# dummy_dishwasher_registration.csv (using get_trainings_data()). Let it depend on the fixture restrict_grid_search().
@pytest.fixture(scope="module")
def trained_dishwasher_model(restrict_grid_search: None) -> Iterator[DishwasherModel]:
    dishwasher_model = DishwasherModel()
    trainings_data = get_trainings_data(file_path=Path(DUMMY_DISHWASHER_REGISTRATION_PATH))
    dishwasher_model.train(data=trainings_data)
    yield dishwasher_model


# -- Exercise 5 --
# Write a test that uses the fixture you just created to test that all predictions on the unlabeled data in
# dummy_dishwasher_registration.csv are positive.
def test_predictions_are_positive(trained_dishwasher_model: DishwasherModel) -> None:
    prediction_data = get_prediction_data(file_path=Path(DUMMY_DISHWASHER_REGISTRATION_PATH))
    predictions = trained_dishwasher_model.predict(data=prediction_data)
    assert (predictions["prediction_dishwashers"] > 0).all()