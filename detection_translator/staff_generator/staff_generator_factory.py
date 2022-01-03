from typing import Type

from detection_translator.common import NotationType
from detection_translator.staff_generator.base_staff_generator import BaseStaffGenerator
from detection_translator.staff_generator.fife_line_staff_generator import FifeLineStaffGenerator


class StaffGeneratorFactory:
    @staticmethod
    def get_staff_generator(notation_type: NotationType) -> Type[BaseStaffGenerator]:
        if notation_type is NotationType.FIFE_STAFF:
            return FifeLineStaffGenerator
        # elif notation_type is NotationType.MENSURAL:
        #     return MensuralStaffGenerator
        else:
            raise NotImplementedError(f'Notation type {notation_type} not implemented')

