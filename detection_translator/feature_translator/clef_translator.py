from typing import List

from detection_translator.common import SubStaff
from detection_translator.constants import CLEFS_CLASSES
from detection_translator.detection import DetectionData
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.clef import Clef
from detection_translator.staff import Staff


class ClefTranslator(BaseFeatureTranslator):

    def __init__(self, staffs: List[Staff], detection_data: DetectionData):
        translator_classes = [k for k, v in detection_data.category_index.items() if v in CLEFS_CLASSES]
        super().__init__(staffs, detection_data, translator_classes)

    def _translate(self, staff: Staff):
        detections = [d for d in self._filtered_detections if d.staff_id == staff.index]

        # get bars from detections
        for bar in staff.bars:
            for det in detections:
                if det not in bar:
                    continue
                _, sub_staff = bar.get_location(det)
                bar.clefs[sub_staff] = Clef(det.det_class)

        # set default keys by previous bar
        prev_clefs = Clef.get_default()
        for bar in staff.bars:
            for section in SubStaff:
                if bar.clefs[section] is None:
                    bar.clefs[section] = prev_clefs[section]
            prev_clefs = bar.clefs



