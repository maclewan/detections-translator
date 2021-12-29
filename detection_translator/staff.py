from typing import List

from detection_translator.constants import LINES_CLASSES, STAFF_CLASS, BRACE_CLASS, IMAGE_WIDTH
from detection_translator.detection import DetectionData, Detection


class StaffFinder:
    _detection_data: DetectionData
    _line_classes: List[int]
    _staff_class: int
    _brace_class: int

    def __init__(self, detection_data: DetectionData):
        self._detection_data = detection_data

        self._generate_line_classes()
        self._generate_staff_class()
        self._generate_brace_class()

    def _generate_line_classes(self) -> None:
        self._line_classes = [c for c, v in self._detection_data.category_index.items() if v in LINES_CLASSES]

    def _generate_brace_class(self) -> None:
        self._brace_class = next(c for c, v in self._detection_data.category_index.items() if v == BRACE_CLASS)

    def _generate_staff_class(self) -> None:
        self._staff_class = next(c for c, v in self._detection_data.category_index.items() if v == STAFF_CLASS)

    def _separate_sections(self) -> List[int]:
        bar_lines = self._detection_data.filter_detection_classes(self._line_classes)
        braces = self._detection_data.filter_detection_classes(self._brace_class)
        staff_bars = self._detection_data.filter_detection_classes(self._staff_class)

        braces = Detection.sort_detections(braces)
        sections = []

        for brace in braces:
            # if brace.box[1] > 0.25 * IMAGE_WIDTH:
            #     continue

            brace_center_y = brace.center[0]
            for s in sections:
                #todo check if brace contains already existing section, if yes than exit
                pass
            sections.append(brace_center_y)

        print(sections)
        return sections

    def find(self) -> None:  # Todo return type
        sections = self._separate_sections()
        # todo
        pass
