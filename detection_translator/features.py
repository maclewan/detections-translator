from enum import Enum

from detection_translator.common import SubStaff


class Clef(Enum):
    G_CLEF = 'clef'
    F_CLEF = 'clef2'

    @classmethod
    def get_default(cls):
        return {
            SubStaff.TOP: cls.G_CLEF,
            SubStaff.BOTTOM: cls.F_CLEF
        }


class Head(Enum):
    HEAD_FULL = 0
    HEAD_EMPTY = 1
