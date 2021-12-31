from dataclasses import dataclass
from typing import Dict, List, Union, Optional
from PIL.Image import Image
from common import Point


@dataclass
class Detection:
    det_class_id: int
    det_class: str
    box: List[int]
    """
    box: y_min, x_min, y_max, x_max
    """

    @property
    def pil_box(self):
        """
        :return: PIL box: [x-min, y-min, x-max, y-max]
        """
        return Detection.to_pil_box(self.box)

    def extended_box(self, delta: int):
        return [self.box[0]-delta, self.box[1]-delta, self.box[2]+delta, self.box[3]+delta]

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
        :return: Tuple(center_y, center_x)
        """
        return Point(self.height // 2 + self.box[0],
                     self.width // 2 + self.box[1])

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

    def contains(self, y: Optional[int] = None, x: Optional[int] = None):
        if y is None and x is None:
            raise ValueError('Point with None coordinates')
        elif y is not None:
            if not (self.box[2] > y > self.box[0]):
                return False
        elif x is not None:
            if not (self.box[3] > x > self.box[1]):
                return False
        return True


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
