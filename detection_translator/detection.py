from dataclasses import dataclass
from typing import Dict, List, Union, Optional, Tuple
from PIL.Image import Image
from detection_translator.common import Point
from detection_translator.constants import OVERLAP_PARAMETER


@dataclass
class Detection:
    det_class_id: int
    det_class: str
    box: List[int]
    staff_id: int = None
    """
    box: y_min, x_min, y_max, x_max
    """

    def translate_x(self, delta: int):
        b = self.box
        self.box = [b[0], b[1] + delta, b[2], b[3] + delta]

    def set_staff(self, staff_id: int):
        self.staff_id = staff_id

    @property
    def pil_box(self):
        """
        :return: PIL box: [x-min, y-min, x-max, y-max]
        """
        return Detection.to_pil_box(self.box)

    def extended_box(self, delta: int):
        return [self.box[0] - delta, self.box[1] - delta, self.box[2] + delta, self.box[3] + delta]

    @staticmethod
    def to_pil_box(box):
        return [b for b in [box[1], box[0], box[3], box[2]]]

    @staticmethod
    def from_pil_box(box):
        return Detection.to_pil_box(box)

    @property
    def height(self) -> int:
        return self.box[2] - self.box[0]

    @property
    def width(self) -> int:
        return self.box[3] - self.box[1]

    @property
    def center(self) -> Point:
        """
        :return: Point(center_y, center_x)
        """
        return Point(self.height // 2 + self.box[0],
                     self.width // 2 + self.box[1])

    def center_translated(self, x_translation=0, y_translation=0) -> Point:
        """
        :param x_translation: percent of detection right if positive, left if negative to translate x
        :param y_translation: percent of detection down if positive, up if negative to translate y
        :return: Point(translated_center_y, translated_center_x)
        """
        return Point(self.height // 2 + self.box[0] + x_translation / 100 * self.height,
                     self.width // 2 + self.box[1] + + y_translation / 100 * self.width)

    def get_section(self, sections_y: List[int]):
        section_distances = []
        for y in sections_y:
            section_distances.append((y, abs(self.center[0] - y)))

        return min(section_distances, key=lambda s: s[1])[0]

    def under(self, point: Point):
        return self.box[0] > point.y

    def above(self, point: Point):
        return self.box[2] < point.y

    @staticmethod
    def sort_detections(detections: List['Detection']) -> List['Detection']:
        return list(sorted(detections, key=lambda d: (d.box[0], d.box[1])))

    def contains(self, y: Optional[int] = None, x: Optional[int] = None, margin: int = 0) -> bool:
        """
        :param y: y coordinate (int)
        :param x: x coordinate (int)
        :param margin: additional margin
        :return: if detection contains given coordinates
        """
        if y is None and x is None:
            raise ValueError('Point with None coordinates')
        elif y is not None:
            if not (self.box[2] + margin > y > self.box[0] - margin):
                return False
        elif x is not None:
            if not (self.box[3] + margin > x > self.box[1] - margin):
                return False
        return True

    @staticmethod
    def filter_multiple_occurrences(detections: List['Detection']) -> List['Detection']:
        to_remove = set()
        for i, det1 in enumerate(detections):

            if i in to_remove:
                continue

            for j, det2 in enumerate(detections):
                if (det1.staff_id != det2.staff_id
                        or i == j
                        or det1.det_class_id != det2.det_class_id
                        or j in to_remove):
                    continue

                overlap, ovlp_prec1, ovlp_prec2 = _check_overlap(det1, det2)
                if not overlap or not (ovlp_prec1 >= ovlp_prec2):
                    continue

                if ovlp_prec2 > OVERLAP_PARAMETER:
                    to_remove.add(j)

        to_return = [d for i, d in enumerate(detections) if i not in to_remove]
        return to_return


@dataclass
class DetectionData:
    image_name: str
    image: Image
    category_index: Dict[int, str]
    detections: List[Detection]

    def filter_detection_classes(self, classes: Union[int, List[int]]) -> List[Detection]:
        if isinstance(classes, list):
            return [d for d in self.detections if d.det_class_id in classes]
        elif isinstance(classes, int):
            return [d for d in self.detections if d.det_class_id == classes]
        else:
            raise RuntimeError('Wrong data type as \'classes\'')


def _check_overlap(det1: Detection, det2: Detection) -> Tuple[bool, Union[int, float], Union[int, float]]:
    """
    rec = [y min, y max, x min, x max]
    returns bool, ovlp_prec1, ovlp_prec2
    """
    box1 = det1.box
    box2 = det2.box
    rec1 = box1[0], box1[2], box1[1], box1[3]
    rec2 = box2[0], box2[2], box2[1], box2[3]

    rec1_area, rec2_area = (rec1[1] - rec1[0]) * (rec1[3] - rec1[2]), (rec2[1] - rec2[0]) * (rec2[3] - rec2[2])

    # Check if intersects
    x1, x2, x3, x4 = rec1[2], rec1[3], rec2[2], rec2[3]
    y1, y2, y3, y4 = rec1[0], rec1[1], rec2[0], rec2[1]

    if y1 > y3:
        y1, y2, y3, y4 = y3, y4, y1, y2
    if x1 > x3:
        x1, x2, x3, x4 = x3, x4, x1, x2

    if x2 - x3 <= 0 or y2 - y3 <= 0:
        return False, 0, 0

    x_sorted, y_sorted = sorted([x1, x2, x3, x4]), sorted([y1, y2, y3, y4])

    a, b = x_sorted[2] - x_sorted[1], y_sorted[2] - y_sorted[1]

    ovlp_area = a * b
    ovlp_prec1, ovlp_prec2 = ovlp_area / rec1_area, ovlp_area / rec2_area
    return True, ovlp_prec1, ovlp_prec2
