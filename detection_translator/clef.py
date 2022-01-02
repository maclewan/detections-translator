from enum import Enum

from detection_translator.common import SubStaff
from detection_translator.note import Note, _Pitch, Octave


class Clef(Enum):
    G_CLEF = 'clef'
    F_CLEF = 'clef2'

    @classmethod
    def get_default(cls):
        return {
            SubStaff.TOP: cls.G_CLEF,
            SubStaff.BOTTOM: cls.F_CLEF
        }

    def get_first_line_note(self):
        if self is Clef.G_CLEF:
            return Note(
                pitch=_Pitch(2),
                octave=Octave.LINE1,
            )
        elif self is Clef.F_CLEF:
            return Note(
                pitch=_Pitch(4),
                octave=Octave.GREAT,
            )



