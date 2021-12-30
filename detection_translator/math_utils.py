from operator import attrgetter
from typing import List
import numpy as np
from sklearn.linear_model import LinearRegression
from common import Point


def find_regression(points: List[Point]):
    points = sorted(points, key=attrgetter('x'))

    x = np.array([p.x for p in points]).reshape((-1, 1))
    y = np.array([p.y for p in points])

    model = LinearRegression()
    model.fit(x, y)
    print(model.coef_)
    print([int(p) for p in model.predict(x)])
    print(y)