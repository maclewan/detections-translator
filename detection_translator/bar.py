from dataclasses import dataclass
from typing import Any, Tuple, List, Optional
from PIL.Image import Image
from detection import Detection
from PIL import ImageEnhance
import numpy as np

from constants import BAR_LINE_FIND_RATIO, END_LINE_FIND_RATIO, BAR_EXTENSION
from detection_translator.common import Point


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

    '''
    Steps:
    - Implement for bar functions checking if detection is inside this bar
    - Implement for bar functions determining on which field/line is note using distances

    '''
    # Todo

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
                and i-1 not in lines_deltas
                and i-2 not in lines_deltas):
            lines_deltas.append(i)
            # stop when all 5 lines found
            if len(lines_deltas) == 5:
                break
    else:
        return None

    distances = [f-s for s, f in zip(lines_deltas[:-1], lines_deltas[1:])]
    return sum(distances)/len(distances)


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
