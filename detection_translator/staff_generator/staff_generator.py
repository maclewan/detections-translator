from abc import ABC
from typing import List
from detection_translator.detection import Detection, DetectionData
from detection_translator.staff import Staff


class BaseStaffGenerator(ABC):
    _detection_data: DetectionData
    _line_classes: List[int]
    _staff_class: int
    _brace_class: int
    _bar_lines: List[Detection]
    _braces: List[Detection]
    _staff_bars: List[Detection]

    def __init__(self, detection_data: DetectionData):
        self._detection_data = detection_data
        pass

    def generate(self) -> List[Staff]:
        pass

    @staticmethod
    def _calculate_avg(distances: List[float]) -> float:
        distances.pop(distances.index(max(distances)))
        distances.pop(distances.index(min(distances)))
        return round(sum(distances) / len(distances), 1)


