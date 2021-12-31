from typing import List, Tuple, Any

from constants import LINES_CLASSES, STAFF_CLASS, BRACE_CLASS, IMAGE_WIDTH
from detection import DetectionData, Detection
from common import Point
from bar import find_bar_y_coordinates, Bar, find_bar_line_distances
from math_utils import find_regression


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
    _avg_lines_distance: float

    def __init__(self, detection_data: DetectionData):
        self._detection_data = detection_data

        self._generate_detection_classes()
        self._get_detections()

    def find(self) -> List[Staff]:
        staff_prototypes = self._generate_staff_prototypes()
        for s in staff_prototypes:
            print(s)
        # todo
        return []

    def _generate_detection_classes(self) -> None:
        self._line_classes = [c for c, v in self._detection_data.category_index.items() if v in LINES_CLASSES]
        self._brace_class = next(c for c, v in self._detection_data.category_index.items() if v == BRACE_CLASS)
        self._staff_class = next(c for c, v in self._detection_data.category_index.items() if v == STAFF_CLASS)

    def _get_detections(self) -> None:
        braces = self._detection_data.filter_detection_classes(self._brace_class)

        self._bar_lines = self._detection_data.filter_detection_classes(self._line_classes)
        self._braces = Detection.sort_detections(braces)
        self._staff_bars = self._detection_data.filter_detection_classes(self._staff_class)

    def _separate_sections(self) -> List[Tuple[int, Detection]]:
        sections = []
        for brace in self._braces:
            if brace.box[1] > 0.25 * IMAGE_WIDTH:
                continue

            brace_center_y = brace.center.y
            for s in sections:
                if brace.contains(y=s[0]):
                    break
            else:
                sections.append((brace_center_y, brace))
        return sections

    def _generate_staff_prototypes(self) -> List[Any]:
        sections = self._separate_sections()
        lines_distances = []
        staff_prototypes = []

        for section, brace in sections:
            bar_lines = [bar for bar in self._bar_lines if bar.contains(y=section)]
            bar_lines.sort(key=lambda b: b.box[1])

            y_ranges = [find_bar_y_coordinates(b, self._detection_data.image) for b in bar_lines]
            lines_distances.extend(
                [d for b in bar_lines if (d := find_bar_line_distances(b, self._detection_data.image)) is not None]
            )

            tops = [Point(x=b.box[1], y=r[0]) for b, r in zip(bar_lines, y_ranges)]
            bottoms = [Point(x=b.box[1], y=r[1]) for b, r in zip(bar_lines, y_ranges)]

            top_line_model = find_regression(tops)
            bottom_line_model = find_regression(bottoms)

            staff_prototypes.append((brace, bar_lines, top_line_model, bottom_line_model))

        # pop max, min, and calculate avg
        lines_distances.pop(lines_distances.index(max(lines_distances)))
        lines_distances.pop(lines_distances.index(min(lines_distances)))
        self._avg_lines_distance = round(sum(lines_distances) / len(lines_distances), 1)

        return staff_prototypes
