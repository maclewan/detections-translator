import numpy as np

import pytest

from detection_translator.bar import Bar, _find_horizontal_lines_distances, _find_horizontal_line_margin
from detection_translator.common import Point, SubStaff
from detection_translator.detection import Detection


def _generate_n_line_image(n):
    white = [255, 255, 255]
    black = [0, 0, 0]
    black_line = [black for _ in range(30)]
    white_line = [white for _ in range(30)]
    data = []
    data.extend([white_line for _ in range(15)])
    for _ in range(n):
        data.extend([black_line])
        data.extend([white_line for _ in range(10)])
    data.extend([white_line for _ in range(3)])

    return np.array(data)


@pytest.fixture
def image_np_0line():
    return _generate_n_line_image(0)


@pytest.fixture
def image_np_5line():
    return _generate_n_line_image(5)


@pytest.fixture
def image_np_1line():
    return _generate_n_line_image(1)


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


def test_get_location(default_bar, detection_head_bottom, detection_head_top, detection_head_under,
                      detection_head_over):
    assert default_bar.get_location(detection_head_bottom) == (0.5, SubStaff.BOTTOM)
    assert default_bar.get_location(detection_head_top) == (3.5, SubStaff.TOP)
    assert default_bar.get_location(detection_head_under) == (-2.0, SubStaff.BOTTOM)
    assert default_bar.get_location(detection_head_over) == (3.0, SubStaff.TOP)


def test_find_bar_y_coords(default_bar, mocker, detection_head_top):
    mocker.patch('detection_translator.bar._find_horizontal_line_margin', return_value=10)
    mocker.patch('detection_translator.bar._prepare_pil_image', return_value=[0, 0, 0])
    assert default_bar.find_bar_y_coordinates(detection_head_top, None) == (5, 5)


def test_find_bar_line_distances(default_bar, mocker, detection_head_top):
    mocker.patch('detection_translator.bar._find_horizontal_lines_distances', return_value=10)
    mocker.patch('detection_translator.bar._prepare_pil_image', return_value=[0, 0, 0])
    assert default_bar.find_bar_line_distances(detection_head_top, None) == 10


def test_find_horizontal_lines(image_np_5line, image_np_1line):
    assert _find_horizontal_lines_distances(image_np_5line, 'bar_line') == 11.0
    assert _find_horizontal_lines_distances(image_np_1line, 'bar_line') is None


def test_find_horizontal_margin(image_np_5line, image_np_0line):
    assert _find_horizontal_line_margin(image_np_5line, 'bar_line', from_top=True) == 15
    assert _find_horizontal_line_margin(image_np_5line, 'bar_line', from_top=False) == 13
    with pytest.raises(ValueError, match='Cannot find staff on bar line'):
        _find_horizontal_line_margin(image_np_0line, 'bar_line', from_top=False)

