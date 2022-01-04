import logging
from pathlib import Path
from typing import Type, List

from detection_translator.data_loader import DataLoader
from detection_translator.detection import DetectionData
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.feature_translator.feature_translator_factory import FeatureTranslatorFactory
from detection_translator.common import NotationType
from detection_translator.music_xml_generator import MusicXmlGenerator
from detection_translator.staff_generator.base_staff_generator import BaseStaffGenerator
from detection_translator.staff_generator.staff_generator_factory import StaffGeneratorFactory

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


class DetectionTranslatorSession:  # pragma: no cover
    _detection_data: DetectionData
    _file: Path
    _image_path: Path
    _staff_generator: Type[BaseStaffGenerator]
    _translators: List[Type[BaseFeatureTranslator]]
    _output_directory: Path

    def __init__(self, file: Path, image_path: Path, notation_type: NotationType, output_directory: Path):
        self._file = file
        self._image_path = image_path
        self._detection_data = self._load_data()
        self._staff_generator = StaffGeneratorFactory.get_staff_generator(notation_type)
        self._translators = FeatureTranslatorFactory.get_translators(notation_type)
        self._output_directory = output_directory

    def _load_data(self) -> DetectionData:
        return DataLoader.load_file(self._file, self._image_path)

    def process(self):
        logging.info('Start finding staffs...')

        staff_finder = self._staff_generator(self._detection_data)
        staffs = staff_finder.generate()

        logging.info('Staffs found!')

        logging.info('Start translation...')

        for Translator in self._translators:
            translator = Translator(staffs, self._detection_data)
            translator.translate()

        logging.info('Translated!')

        logging.info('Start generating xml files')

        for i, staff in enumerate(staffs):
            mxml_generator = MusicXmlGenerator(staff)
            mxml_generator.generate(name=f'{self._output_directory}/{str(self._image_path.name).split(".")[0]}_staff{i}')

            logging.info(f'File {str(self._image_path.name).split(".")[0]}_staff{i}.musicxml generated')
