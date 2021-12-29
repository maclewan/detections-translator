from pathlib import Path

from data_loader import DetectionData, load_data


class Translator:
    _detection_data: DetectionData
    _file: Path

    def __init__(self, file: Path):
        self._file = file
        self._detection_data = self._load_data()

    def _load_data(self) -> DetectionData:
        return load_data(self._file)

    def translate(self):

        pass