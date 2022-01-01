from pathlib import Path
from typing import Type, List

from data_loader import DataLoader
from detection import DetectionData
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.feature_translator.cleff_translator import CleffTranslator
from detection_translator.notation import NotationType
from detection_translator.staff_generator.base_staff_generator import BaseStaffGenerator
from detection_translator.staff_generator.staff_generator_factory import StaffGeneratorFactory


class DetectionTranslatorSession:
    _detection_data: DetectionData
    _file: Path
    _image_path: Path
    _staff_generator: Type[BaseStaffGenerator]
    _translators: List[Type[BaseFeatureTranslator]]

    def __init__(self, file: Path, image_path: Path, notation_type: NotationType):
        self._file = file
        self._image_path = image_path
        self._detection_data = self._load_data()
        self._staff_generator = StaffGeneratorFactory.get_staff_generator(notation_type)

    def _load_data(self) -> DetectionData:
        return DataLoader.load_file(self._file, self._image_path)

    def process(self):
        staff_finder = self._staff_generator(self._detection_data)
        staffs = staff_finder.generate()

        ## Test:
        ct = CleffTranslator(staffs, self._detection_data, [1, 2])
        ct.translate()


        # det = self._detection_data.filter_detection_classes(3)
        # det = [d for d in det if d in staffs[0].bars[0]]
        # print(staffs[0].bars[0])
        #
        # for d in det:
        #     t = staffs[0].bars[0].get_location(d)
        #     print(t, d)

        # for d in self._detection_data.filter_detection_classes(11):
        #     if (d in staffs[2].bars[1]):
        #         print(True, d)

        print('Done')