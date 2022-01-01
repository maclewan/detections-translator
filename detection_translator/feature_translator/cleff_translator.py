from typing import List

from detection_translator.detection import DetectionData
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.staff import Staff


class CleffTranslator(BaseFeatureTranslator):

    def __init__(self, staffs: List[Staff], detection_data: DetectionData, translator_classes: List[int]):
        super().__init__(staffs, detection_data, translator_classes)

    def _translate(self, staff: Staff):
        staff.test = True
        pass

