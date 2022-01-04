from detection_translator.common import NotationType
from detection_translator.staff_generator.fife_line_staff_generator import FifeLineStaffGenerator
from detection_translator.staff_generator.staff_generator_factory import StaffGeneratorFactory


def test_staff_generator_factory():
    assert StaffGeneratorFactory.get_staff_generator(NotationType.FIFE_STAFF) == FifeLineStaffGenerator