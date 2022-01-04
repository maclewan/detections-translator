from typing import List, Callable
import numpy as np
from sklearn.linear_model import LinearRegression
from detection_translator.common import Point


def find_regression(points: List[Point]) -> LinearRegression:  # pragma: no cover
    x = np.array([p.x for p in points]).reshape((-1, 1))
    y = np.array([p.y for p in points])
    model = LinearRegression()
    model.fit(x, y)
    return model


def get_polynomial_predictor(start: Point, end: Point) -> Callable:
    x = np.array([start.x, end.x])
    y = np.array([start.y, end.y])
    predictor = np.poly1d(np.polyfit(x, y, 1))
    return lambda new_x: round(float(predictor(new_x)), 2)
