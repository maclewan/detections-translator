import pytest

from detection_translator.bar import Bar
from detection_translator.clef import Clef
from detection_translator.common import Point, SubStaff
from detection_translator.detection import Detection
from detection_translator.feature_translator.note_translator import NoteTranslator
from detection_translator.note import _Pitch, Rest


@pytest.fixture
def default_bar():
    bar = Bar(
        left_bottom=Point(y=301, x=237),
        left_top=Point(y=118, x=237),
        right_bottom=Point(y=301, x=480),
        right_top=Point(y=118, x=480),
        lines_count=5,
        line_distance=13.0,
        is_start=True,
        is_end=False,
        clefs=None,
        sections=[],
    )
    bar.clefs = {
        SubStaff.TOP: Clef('clef'),
        SubStaff.BOTTOM: Clef('clef2')
    }

    return bar


@pytest.fixture
def reference_sections():
    return [
        [Detection(det_class_id=3, det_class='head1', box=[143, 328, 158, 346], staff_id=0),
         Detection(det_class_id=3, det_class='head1', box=[164, 330, 180, 348], staff_id=0),
         Detection(det_class_id=3, det_class='head1', box=[228, 331, 243, 348], staff_id=0)],
        [Detection(det_class_id=3, det_class='head1', box=[136, 425, 152, 440], staff_id=0)]
    ]


@pytest.fixture
def detections():
    return [
        Detection(det_class_id=3, det_class='head1', box=[143, 328, 158, 346], staff_id=0),
        Detection(det_class_id=3, det_class='head1', box=[143, 328, 169, 371], staff_id=0),
        Detection(det_class_id=3, det_class='head1', box=[164, 330, 180, 348], staff_id=0),
        Detection(det_class_id=3, det_class='head1', box=[228, 331, 243, 348], staff_id=0),
        Detection(det_class_id=3, det_class='head1', box=[122, 540, 138, 558], staff_id=0),
        Detection(det_class_id=3, det_class='head1', box=[140, 542, 157, 559], staff_id=0),
        Detection(det_class_id=3, det_class='head1', box=[136, 425, 152, 440], staff_id=0)
    ]


def test_generate_sections(default_bar, detections, reference_sections):
    assert NoteTranslator._generate_sections(default_bar, detections) == reference_sections


def test_translate_detection(default_bar, reference_sections):
    detection = reference_sections[0][0]
    assert NoteTranslator._translate_detection(detection, default_bar).pitch is _Pitch(5)
    detection.det_class = 'pause1'
    assert NoteTranslator._translate_detection(detection, default_bar) == Rest(sub_staff=SubStaff.TOP, duration=1)
