import pytest as pytest

from detection_translator.common import Point
from detection_translator.detection import Detection


@pytest.fixture
def default_detection():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[10, 10, 100, 150],
        staff_id=0,
    )


@pytest.fixture
def default_detection1():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[10, 10, 100, 152],
        staff_id=1,
    )


@pytest.fixture
def default_detection2():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[5010, 5010, 5100, 5152],
        staff_id=1,
    )


def test_translate_x(default_detection):
    default_detection.translate_x(10)
    assert default_detection.box == [10, 20, 100, 160]


def test_set_staff_id(default_detection):
    default_detection.set_staff(2137)
    assert default_detection.staff_id == 2137


def test_to_pil_box(default_detection):
    assert Detection.to_pil_box(default_detection.box) == [10, 10, 150, 100]
    assert default_detection.pil_box == [10, 10, 150, 100]
    assert Detection.from_pil_box(default_detection.box) == [10, 10, 150, 100]


def test_center_translated(default_detection):
    assert default_detection.center_translated(21, 37) == Point(y=73.9, x=131.8)


def test_get_sections(default_detection):
    assert default_detection.get_section([40, 140, 300, 50, 45]) == 50


def test_under_above(default_detection):
    assert default_detection.above(Point(210, 370))
    assert default_detection.under(Point(-5, -100))


def test_contains(default_detection):
    with pytest.raises(ValueError):
        default_detection.contains()
    assert not default_detection.contains(x=5)
    assert default_detection.contains(x=15)
    assert not default_detection.contains(y=5)
    assert default_detection.contains(y=15)
    assert not default_detection.contains(y=5, x=15)
    assert default_detection.contains(y=15, x=15)


def test_filter_multiple(default_detection, default_detection1, default_detection2):
    assert Detection.filter_multiple_occurrences([default_detection]*2) == [default_detection]
    assert Detection.filter_multiple_occurrences(
        [default_detection, default_detection1, default_detection2]) == [default_detection, default_detection1, default_detection2]


def test_wtf():
    d = Detection(
        det_class='head1',
        det_class_id=1,
        box=[106, 327, 163, 352],
        staff_id=0,
    )
    assert d.contains(y=150, x=337)
