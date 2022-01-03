import pytest

from detection_translator.bar import Bar
from detection_translator.common import Point, SubStaff
from detection_translator.detection import Detection


@pytest.fixture
def default_bar():
    return Bar(
        left_bottom=Point(250, 0),
        left_top=Point(0, 0),
        right_top=Point(0, 450),
        right_bottom=Point(250, 450),
        lines_count=5,
        line_distance=10,
        is_start=False,
        is_end=False,
    )


@pytest.fixture
def detection_head_top():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[0, 0, 10, 10]
    )


@pytest.fixture
def detection_head_bottom():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[240, 0, 250, 10]
    )

@pytest.fixture
def detection_head_under():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[265, 0, 275, 10]
    )

@pytest.fixture
def detection_head_over():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[-15, 0, -5, 10]
    )

@pytest.fixture
def detection_head_outside():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[1000, 1005, 1010, 1015]
    )


@pytest.fixture
def detection_head_outside2():
    return Detection(
        det_class='head1',
        det_class_id=1,
        box=[1000, 0, 1050, 10]
    )


def test_center(default_bar):
    center = default_bar.center_y
    assert center == 125


def test_detection_center(detection_head_top):
    center = Bar._detection_center(detection_head_top)
    assert center == Point(5, 5)


def test_contains(default_bar, detection_head_top, detection_head_outside, detection_head_outside2):
    assert detection_head_top in default_bar
    assert detection_head_outside not in default_bar
    assert detection_head_outside2 not in default_bar


def test_get_location(default_bar, detection_head_bottom, detection_head_top, detection_head_under, detection_head_over):
    assert default_bar.get_location(detection_head_bottom) == (0.5, SubStaff.BOTTOM)
    assert default_bar.get_location(detection_head_top) == (3.5, SubStaff.TOP)
    assert default_bar.get_location(detection_head_under) == (-2.0, SubStaff.BOTTOM)
    assert default_bar.get_location(detection_head_over) == (3.0, SubStaff.TOP)




