from collections import namedtuple
from enum import Enum

Point = namedtuple('Point', ['y', 'x'])


class SubStaff(Enum):
    TOP = 0
    BOTTOM = 1


class NotationType(Enum):
    FIFE_STAFF = 0
    # MENSURAL = 1