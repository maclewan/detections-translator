from dataclasses import dataclass
from typing import Any, Tuple, List, Optional, Union
from PIL.Image import Image
from detection import Detection
from PIL import ImageEnhance
import numpy as np

from constants import BAR_LINE_FIND_RATIO, END_LINE_FIND_RATIO, BAR_EXTENSION, MAX_ADDED_LINES, CENTER_FUNCTIONS
from detection_translator.common import Point, SubStaff
from detection_translator.math_utils import get_polynomial_predictor


@dataclass
class Bar:
    left_bottom: Point
    left_top: Point
    right_bottom: Point
    right_top: Point
    lines_count: int
    line_distance: int
    is_start: bool
    is_end: bool

    def __post_init__(self):
        self._top_line_predictor = get_polynomial_predictor(self.left_top, self.right_top)
        self._bottom_line_predictor = get_polynomial_predictor(self.left_bottom, self.right_bottom)

    @property
    def center_y(self) -> int:
        return self.left_top.y + (self.right_bottom.y - self.left_top.y) // 2

    @staticmethod
    def _detection_center(detection: Detection):
        return CENTER_FUNCTIONS[detection.det_class](detection)

    def __contains__(self, detection: Detection):
        center = self._detection_center(detection)

        if not (self.left_bottom.x < center.x < self.right_top.x):
            return False
        if not (self.left_top.y - self.line_distance * MAX_ADDED_LINES < center.y
                < self.right_bottom.y + self.line_distance * MAX_ADDED_LINES):
            return False
        return True

    def get_location(self, detection: Detection):
        center = self._detection_center(detection)
        if center.y < self.center_y:
            sub_staff = SubStaff.TOP
            y_pred = self._top_line_predictor(detection.center.x)
            bottom_line_y = y_pred + self.line_distance * (self.lines_count - 1)
        else:
            sub_staff = SubStaff.BOTTOM
            bottom_line_y = self._bottom_line_predictor(detection.center.x)
        line = self._get_line_number(bottom_line_y, detection.center.y)
        return line, sub_staff

    def _get_line_number(self, bottom_line_y: float, detection_y: Union[int, float]):
        result = (bottom_line_y - detection_y) / self.line_distance
        return (round(result * 2) / 2) + 1

    @staticmethod
    def find_bar_y_coordinates(bar: Detection, image: Image) -> Tuple[int, int]:
        """
        :param bar: detected Bar
        :param image: whole PIL image
        :return: y_min, y_max
        """
        extended_box = bar.extended_box(BAR_EXTENSION)
        prepared_image = _prepare_pil_image(extended_box, image)
        image_np = np.array(prepared_image)

        top_margin = _find_horizontal_line_margin(image_np, bar.det_class, from_top=True)
        bottom_margin = _find_horizontal_line_margin(image_np, bar.det_class, from_top=False)

        return extended_box[0] + top_margin, extended_box[2] - bottom_margin

    @staticmethod
    def find_bar_line_distances(bar: Detection, image: Image) -> float:
        extended_box = bar.extended_box(BAR_EXTENSION)
        prepared_image = _prepare_pil_image(extended_box, image)
        image_np = np.array(prepared_image)

        distance = _find_horizontal_lines_distances(image_np, bar.det_class)
        return distance


def _find_horizontal_lines_distances(image_np: Any, detection_class: str) -> Optional[float]:
    find_ratio = BAR_LINE_FIND_RATIO if detection_class == 'bar_line' else END_LINE_FIND_RATIO
    lines_deltas = []

    for i, y in enumerate(image_np):
        black_ctr, white_ctr = 0, 0
        for x in y:
            if x.tolist() == [255, 255, 255]:
                white_ctr += 1
            else:
                black_ctr += 1
        black_coverage = black_ctr / (black_ctr + white_ctr)
        # check if two previous are not counted as line
        if (black_coverage >= find_ratio
                and i - 1 not in lines_deltas
                and i - 2 not in lines_deltas):
            lines_deltas.append(i)
            # stop when all 5 lines found
            if len(lines_deltas) == 5:
                break
    else:
        return None

    distances = [f - s for s, f in zip(lines_deltas[:-1], lines_deltas[1:])]
    return sum(distances) / len(distances)


def _find_horizontal_line_margin(image_np: Any, detection_class: str, from_top: bool = True) -> int:
    direction = 1 if from_top else -1
    find_ratio = BAR_LINE_FIND_RATIO if detection_class == 'bar_line' else END_LINE_FIND_RATIO

    for i, y in enumerate(image_np[::direction]):
        black_ctr, white_ctr = 0, 0
        for x in y:
            if x.tolist() == [255, 255, 255]:
                white_ctr += 1
            else:
                black_ctr += 1
        black_coverage = black_ctr / (black_ctr + white_ctr)
        if black_coverage >= find_ratio:
            return i
    else:
        raise ValueError('Cannot find staff on bar line')


def _prepare_pil_image(extended_box: List[int], image: Image) -> Image:
    extended_pil_box = Detection.to_pil_box(extended_box)
    cropped = image.crop(extended_pil_box)
    cropped = ImageEnhance.Contrast(cropped).enhance(6.0)
    return ImageEnhance.Brightness(cropped).enhance(2.0)

# Todo: test me
