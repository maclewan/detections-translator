from abc import ABC, abstractmethod
from typing import List

from detection_translator.detection import DetectionData, Detection
from detection_translator.staff import Staff


class BaseFeatureTranslator(ABC):
    _staffs: List[Staff]
    _detection_data: DetectionData
    _translator_classes: List[int]
    _filtered_detections: List[Detection]

    @abstractmethod
    def __init__(self, staffs: List[Staff], detection_data: DetectionData, translator_classes: List[int]):
        self._staffs = staffs
        self._detection_data = detection_data
        self._translator_classes = translator_classes
        self._filter_detections()
        pass

    def _filter_detections(self):
        detections = self._detection_data.filter_detection_classes(self._translator_classes)
        self._update_detection_staff(detections)
        detections = Detection.filter_multiple_occurrences(detections)
        detections.sort(key=lambda d: d.center.x)
        self._filtered_detections = detections

    def _update_detection_staff(self, detections: List[Detection]):
        for det in detections:
            staff_id = next(staff for staff in self._staffs if det in staff).index
            det.set_staff(staff_id)

    def translate(self):
        for staff in self._staffs:
            self._translate(staff)

    @abstractmethod
    def _translate(self, staff: Staff):
        pass
