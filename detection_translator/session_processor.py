from pathlib import Path

from data_loader import DataLoader
from detection import DetectionData
from fife_line_staff_generator import FifeLineStaffGenerator


class SessionProcessor:
    _detection_data: DetectionData
    _file: Path
    _image_path: Path

    def __init__(self, file: Path, image_path: Path):
        self._file = file
        self._image_path = image_path
        self._detection_data = self._load_data()

    def _load_data(self) -> DetectionData:
        return DataLoader.load_file(self._file, self._image_path)

    def process(self):
        staff_finder = FifeLineStaffGenerator(self._detection_data)
        staffs = staff_finder.find()
