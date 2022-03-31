import os
from pathlib import Path

from dishwashers.data import get_prediction_data, get_trainings_data
from dishwashers.model import DishwasherModel

DISHWASHER_REGISTRATION_PATH = Path(os.environ.get("DISHWASHER_REGISTRATION_PATH", "data/dishwasher_registration.csv"))
PREDICTIONS_PATH = Path(os.environ.get("PREDICTIONS_PATH", "data/dishwasher_predictions.csv"))


def main() -> None:
    trainings_data = get_trainings_data(file_path=DISHWASHER_REGISTRATION_PATH)
    prediction_data = get_prediction_data(file_path=DISHWASHER_REGISTRATION_PATH)
    model = DishwasherModel()
    model.train(data=trainings_data)
    predictions = model.predict(data=prediction_data)
    predictions.to_csv(PREDICTIONS_PATH, index=False)


if __name__ == "__main__":
    main()
