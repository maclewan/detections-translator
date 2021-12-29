from pathlib import Path
from json import loads
from typing import Dict, Any, List

from constants import IMAGE_HEIGHT as HEIGHT, IMAGE_WIDTH as WIDTH
from detection_translator.detection import DetectionData, Detection


class DataLoader:

    @staticmethod
    def load_file(file: Path) -> DetectionData:
        data: Dict[str, Any] = loads(file.read_text())

        image = data.get('image', None)
        category_index: Dict[str, Any] = data.get('category_index', None)
        detections = data.get('detections', None)

        if not (image and category_index and detections):
            raise RuntimeError('Missing data in json')

        detection_data = DetectionData(
            image=image,
            category_index={v['id']: v['name'] for k, v in category_index.items()},
            detections=[Detection(
                det_class=d['class'],
                box=[int(i) for i in
                     [d['box'][0] * HEIGHT, d['box'][1] * WIDTH, d['box'][2] * HEIGHT, d['box'][3] * WIDTH]
                     ]
            ) for d in detections]
        )

        return detection_data

    @staticmethod
    def load_files(files: List[Path]) -> List[DetectionData]:
        raise NotImplementedError
