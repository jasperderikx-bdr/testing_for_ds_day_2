import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV, train_test_split
from sklearn.pipeline import Pipeline

from dishwashers.data import AddRecipeDuration


class DishwasherModel:
    def __init__(self) -> None:
        self.estimator = None
        self.test_score = None

    def train(self, data: pd.DataFrame) -> None:
        x = data.drop(["dishwashers"], axis=1)
        y = data["dishwashers"]
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=37)

        # Define model pipeline.
        pipeline = Pipeline([("add_recipe_duration", AddRecipeDuration()),
                             ("RFR", RandomForestRegressor())])

        # Determine best hyper parameters.
        grid = GridSearchCV(pipeline,
                            param_grid={"RFR__max_depth": [2, 4, 8, 16],
                                        "RFR__n_estimators": [25, 50, 100, 200, 400]},
                            cv=10)
        grid.fit(x_train, y_train)

        self.test_score = grid.best_estimator_.score(x_test, y_test)

        # Train on all labeled data.
        grid.best_estimator_.fit(x, y)

        self.estimator = grid.best_estimator_

    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        data_ = data.copy()
        data_["prediction_dishwashers"] = self.estimator.predict(data_)
        return data_
