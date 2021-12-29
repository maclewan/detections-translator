from pathlib import Path

from data_loader import DataLoader
from detection import DetectionData
from staff import StaffFinder


class Translator:
    _detection_data: DetectionData
    _file: Path

    def __init__(self, file: Path):
        self._file = file
        self._detection_data = self._load_data()

    def _load_data(self) -> DetectionData:
        return DataLoader.load_file(self._file)

    def translate(self):
        staff_finder = StaffFinder(self._detection_data)
        staff_finder.find()
