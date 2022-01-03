from pathlib import Path
from typing import Type, List

from data_loader import DataLoader
from detection import DetectionData
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.feature_translator.clef_translator import ClefTranslator
from detection_translator.feature_translator.note_translator import NoteTranslator
from detection_translator.common import NotationType
from detection_translator.music_xml_generator import MusicXmlGenerator
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
        ct = ClefTranslator(staffs, self._detection_data)
        ct.translate()

        nt = NoteTranslator(staffs, self._detection_data)
        nt.translate()

        for i, staff in enumerate(staffs):
            mxml_generator = MusicXmlGenerator(staff)
            mxml_generator.generate(name=f'{str(self._image_path.name).split(".")[0]}_staff{i}')

        print('Done')
