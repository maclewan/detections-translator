from dataclasses import dataclass
from typing import List, Tuple, NewType, NamedTuple
from sklearn.linear_model import LinearRegression
from detection_translator.common import Point
from detection_translator.bar import Bar
from detection_translator.detection import Detection


class StaffPrototype(NamedTuple):
    brace: Detection
    bar_lines: List[Detection]
    tops: List[Point]
    bottoms: List[Point]
    top_line_model: LinearRegression
    bottom_line_model: LinearRegression


@dataclass
class Staff:
    index: int
    bars: List[Bar]

