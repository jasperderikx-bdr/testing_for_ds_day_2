import pandas as pd
from sklearn.linear_model import LinearRegression, RidgeCV
from src.data import read_input_data
from datetime import *


def train_model():
    data = read_input_data()
    x = data[["colleagues"]]
    y = data[["dishwashers"]]
    reg = LinearRegression(fit_intercept=False, positive=True).fit(x, y)
    return dict(zip(reg.feature_names_in_,
                    [round(c, 3) for c in reg.coef_]))


if __name__ == "__main__":
    print(train_model())
