from typing import List

from detection_translator.constants import LINES_CLASSES, STAFF_CLASS
from detection_translator.data_loader import DetectionData, Detection


class StaffFinder:
    _detection_data: DetectionData
    _line_classes: List[int]
    _staff_class: int

    def __init__(self, detection_data: DetectionData):
        self._detection_data = detection_data

        self._generate_line_classes()
        self._generate_staff_class()

    def _generate_line_classes(self) -> None:
        self._line_classes = [c for c, v in self._detection_data.category_index.items() if v in LINES_CLASSES]

    def _generate_staff_class(self) -> None:
        self._staff_class = next(c for c, v in self._detection_data.category_index.items() if v == STAFF_CLASS)

    def _separate_sections(self) -> List[Detection]:
        bar_lines = self._detection_data.filter_detection_classes(self._line_classes)


        pass

    def find(self) -> None: # Todo return type
        sections = self._separate_sections()
        pass
