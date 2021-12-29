from dataclasses import dataclass
from pathlib import Path
from json import loads
from typing import Dict, Any, List, Union


@dataclass
class Detection:
    det_class: int
    box: List[int]


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


def load_data(file: Path) -> DetectionData:
    data: Dict[str, Any] = loads(file.read_text())

    image = data.get('image', None)
    category_index: Dict[str, Any] = data.get('category_index', None)
    detections = data.get('detections', None)

    if not (image and category_index and detections):
        raise RuntimeError('Missing data in json')

    detection_data = DetectionData(
        image=image,
        category_index={v['id']: v['name'] for k, v in category_index.items()},
        detections=[Detection(det_class=d['class'], box=d['box']) for d in detections]
    )

    return detection_data
