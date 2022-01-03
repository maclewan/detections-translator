from typing import List, Tuple
import numpy as np
from detection_translator.constants import LINES_CLASSES, STAFF_CLASS, BRACE_CLASS, IMAGE_WIDTH
from detection_translator.detection import DetectionData, Detection
from detection_translator.common import Point
from detection_translator.bar import Bar
from detection_translator.staff_generator.base_staff_generator import Staff, BaseStaffGenerator
from detection_translator.math_utils import find_regression
from detection_translator.staff import StaffPrototype


class FifeLineStaffGenerator(BaseStaffGenerator):
    _lines_count = 5
    _avg_lines_distance: int

    def __init__(self, detection_data: DetectionData):
        super().__init__(detection_data)

        self._generate_detection_classes()
        self._get_detections()

    def generate(self) -> List[Staff]:
        staff_prototypes = self._generate_staff_prototypes()
        staffs = [self._create_staff_from_prototype(i, staff_prototype)
                  for i, staff_prototype in enumerate(staff_prototypes)]

        return staffs

    def _create_staff_from_prototype(self, index: int, prototype: StaffPrototype) -> Staff:
        # Generate first bar
        brace_x = prototype.brace.box[3]
        np_brace_x = np.array(brace_x).reshape(-1, 1)
        start_top = Point(y=int(prototype.top_line_model.predict(np_brace_x)[0]), x=brace_x)
        start_bottom = Point(y=int(prototype.bottom_line_model.predict(np_brace_x)[0]), x=brace_x)
        first_bar = self._create_bar(prototype.brace, prototype.bar_lines[0],
                                     [start_top, prototype.tops[0]], [start_bottom, prototype.bottoms[0]])
        # Generate remaining bars
        bars = [first_bar]
        for i in range(len(prototype.bar_lines) - 1):
            bar = self._create_bar(prototype.bar_lines[i], prototype.bar_lines[i + 1],
                                   prototype.tops[i:i + 2], prototype.bottoms[i:i + 2])
            bars.append(bar)

        return Staff(index, bars)

    def _create_bar(self, start: Detection, end: Detection, tops: List[Point], bottoms: List[Point]) -> Bar:
        return Bar(
            left_bottom=bottoms[0],
            left_top=tops[0],
            right_bottom=bottoms[1],
            right_top=tops[1],
            lines_count=self._lines_count,
            line_distance=self._avg_lines_distance,
            is_start=start.det_class == 'brace',
            is_end=end.det_class == 'end_line'
        )

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

    def _generate_staff_prototypes(self) -> List[StaffPrototype]:
        sections = self._separate_sections()
        lines_distances = []
        staff_prototypes = []

        for section, brace in sections:
            bar_lines = [bar for bar in self._bar_lines if bar.contains(y=section)]
            bar_lines.sort(key=lambda b: b.box[1])
            # move last line left
            bar_lines[-1].translate_x(delta=-bar_lines[-1].width//2)
            y_ranges = [Bar.find_bar_y_coordinates(b, self._detection_data.image) for b in bar_lines]
            lines_distances.extend(
                [d for b in bar_lines if (d := Bar.find_bar_line_distances(b, self._detection_data.image)) is not None]
            )

            tops = [Point(x=b.center.x, y=r[0]) for b, r in zip(bar_lines, y_ranges)]
            bottoms = [Point(x=b.center.x, y=r[1]) for b, r in zip(bar_lines, y_ranges)]
            top_line_model = find_regression(tops)
            bottom_line_model = find_regression(bottoms)

            staff_prototypes.append(StaffPrototype(brace, bar_lines, tops, bottoms,
                                                   top_line_model, bottom_line_model))

        self._avg_lines_distance = self._calculate_avg(lines_distances)
        return staff_prototypes
