import pytest as pytest

from detection_translator.common import Point
from detection_translator.detection import Detection


@pytest.fixture
def default_detection():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[100, 150, 10, 10]
    )


def test_translate_x(default_detection):
    default_detection.translate_x(10)
    assert default_detection.box == [100, 160, 10, 20]


def test_set_staff_id(default_detection):
    default_detection.set_staff(2137)
    assert default_detection.staff_id == 2137


def test_to_pil_box(default_detection):
    assert Detection.to_pil_box(default_detection.box) == [150, 100, 10, 10]
    assert default_detection.pil_box == [150, 100, 10, 10]
    assert Detection.from_pil_box(default_detection.box) == [150, 100, 10, 10]


def test_center_translated(default_detection):
    assert default_detection.center_translated(21, 37) == Point(y=36.1, x=28.2)


def test_get_sections(default_detection):
    assert default_detection.get_section([40, 140, 300, 50, 45]) == 50
