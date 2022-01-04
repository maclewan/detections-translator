BRACE_CLASS = 'brace'
LINES_CLASSES = ['end_line', 'bar_line']
STAFF_CLASS = 'staff'
CLEFS_CLASSES = ['clef', 'clef2']
NOTE_CLASSES = ['head1', 'head2', 'pause1']
RHYTHM_CLASSES = ['quater', 'quaterdot', 'eight1', 'eight2', 'sixteenth']

IMAGE_HEIGHT = 1320
IMAGE_WIDTH = 1868

BAR_EXTENSION = 5
BAR_LINE_FIND_RATIO = 0.7
END_LINE_FIND_RATIO = 0.55

OVERLAP_PARAMETER = 0.85

HEAD_AREA_MARGIN = 2.4

MAX_ADDED_LINES = 2
CENTERED_CLASSES = ['sign1', 'sign3'] + NOTE_CLASSES + CLEFS_CLASSES + RHYTHM_CLASSES
CENTER_FUNCTIONS = {
    c: (lambda detection: detection.center) for c in CENTERED_CLASSES
}
CENTER_FUNCTIONS['sign2'] = lambda detection: detection.center_translated(x_translation=25, y_translation=0)

CLASSES_TO_DURATION = {
    'quater': 1.0,
    'quaterdot': 1.5,
    'eight1': 0.5,
    'eight2': 0.5,
    'sixteenth': 0.25,
}
