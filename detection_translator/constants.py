from detection_translator.common import SubStaff
from detection_translator.clef import Clef

DATA_PATH = 'data'
BRACE_CLASS = 'brace'
LINES_CLASSES = ['end_line', 'bar_line']
STAFF_CLASS = 'staff'
CLEFS_CLASSES = ['clef', 'clef2']
NOTE_CLASSES = ['head1', 'head2']

IMAGE_HEIGHT = 1320
IMAGE_WIDTH = 1868

BAR_EXTENSION = 5
BAR_LINE_FIND_RATIO = 0.45
END_LINE_FIND_RATIO = 0.45

OVERLAP_PARAMETER = 0.85

HEAD_AREA_MARGIN = 2.3

MAX_ADDED_LINES = 2
CENTERED_CLASSES = ['head1', 'head2', 'sign1', 'sign3', 'clef', 'clef2']
CENTER_FUNCTIONS = {
    c: (lambda detection: detection.center) for c in CENTERED_CLASSES
}
CENTER_FUNCTIONS['sign2'] = lambda detection: detection.center_translated(x_translation=25, y_translation=0)


