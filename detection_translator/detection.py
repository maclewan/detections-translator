from dataclasses import dataclass
from typing import Dict, List, Union, Tuple, Optional


class Detection:
    pass


@dataclass
class Detection:
    det_class: int
    box: List[int]

    @property
    def height(self) -> int:
        return self.box[2] - self.box[0]

    @property
    def width(self) -> int:
        return self.box[3] - self.box[1]

    @property
    def center(self) -> Tuple[int, int]:
        """
        :return: Tuple(center_y, center_x)
        """
        return (self.height // 2 + self.box[0],
                self.width // 2 + self.box[1])

    @staticmethod
    def sort_detections(detections: List[Detection]) -> List[Detection]:
        return list(sorted(detections, key=lambda d: (d.box[0], d.box[1])))

    def contains(self, y: Optional[int] = None, x: Optional[int] = None):
        if y is None and x is None:
            raise ValueError('Point with None coordinates')
        # todo: implement contain function



@dataclass
class DetectionData:
    image: str
    category_index: Dict[int, str]
    detections: List[Detection]

    def filter_detection_classes(self, classes: Union[int, List[int]]) -> List[Detection]:
        if isinstance(classes, list):
            return [d for d in self.detections if d.det_class in classes]
        elif isinstance(classes, int):
            return [d for d in self.detections if d.det_class == classes]
        else:
            raise RuntimeError('Wrong data type as \'classes\'')
