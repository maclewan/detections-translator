from typing import List, Tuple

from constants import LINES_CLASSES, STAFF_CLASS, BRACE_CLASS, IMAGE_WIDTH
from detection import DetectionData, Detection
from common import Point
from math_utils import find_regression


class Bar:
    _left_bottom: Tuple[int, int]
    _left_top: Tuple[int, int]
    _right_bottom: Tuple[int, int]
    _right_top: Tuple[int, int]

    def __init__(self):
        pass


class Staff:
    _bars = List[Bar]

    def __init__(self):
        pass


class StaffFinder:
    _detection_data: DetectionData
    _line_classes: List[int]
    _staff_class: int
    _brace_class: int
    _bar_lines: List[Detection]
    _braces: List[Detection]
    _staff_bars: List[Detection]

    def __init__(self, detection_data: DetectionData):
        self._detection_data = detection_data

        self._generate_detection_classes()
        self._get_detections()

    def _generate_detection_classes(self) -> None:
        self._line_classes = [c for c, v in self._detection_data.category_index.items() if v in LINES_CLASSES]
        self._brace_class = next(c for c, v in self._detection_data.category_index.items() if v == BRACE_CLASS)
        self._staff_class = next(c for c, v in self._detection_data.category_index.items() if v == STAFF_CLASS)

    def _get_detections(self) -> None:
        braces = self._detection_data.filter_detection_classes(self._brace_class)

        self._bar_lines = self._detection_data.filter_detection_classes(self._line_classes)
        self._braces = Detection.sort_detections(braces)
        self._staff_bars = self._detection_data.filter_detection_classes(self._staff_class)

    def _separate_sections(self) -> List[int]:
        sections = []
        for brace in self._braces:
            if brace.box[1] > 0.25 * IMAGE_WIDTH:
                continue

            brace_center_y = brace.center.y
            for s in sections:
                if brace.contains(y=s):
                    break
            else:
                sections.append(brace_center_y)

        return sections

    def find(self) -> None:  # Todo return type
        sections = self._separate_sections()
        for section in sections:
            bar_lines = [bar for bar in self._bar_lines if bar.contains(y=section)]
            staffs = [staff for staff in self._staff_bars
                      if staff.get_section(sections) == section and staff.center.x < 0.25 * IMAGE_WIDTH]

            left_bottoms = ([Point(y=bar.box[2], x=bar.box[1]) for bar in bar_lines] +
                            [Point(y=staff.box[2], x=staff.box[1]) for staff in staffs
                             if staff.under(Point(y=section, x=0))])

            #print(left_bottoms)
            find_regression(left_bottoms)
            # print(sorted(left_bottoms, key=lambda x: x[1]))

        # todo
        pass
