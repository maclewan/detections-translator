from detection_translator.clef import Clef
from detection_translator.common import SubStaff
from detection_translator.note import Note, _Pitch, Octave


def test_clef_get_default():
    defaults = Clef.get_default()
    assert defaults == {
        SubStaff.TOP: Clef.G_CLEF,
        SubStaff.BOTTOM: Clef.F_CLEF
    }


def test_get_first_line_note():
    clef_g = Clef('clef')
    assert clef_g.get_first_line_note() == Note(
        pitch=_Pitch(2),
        octave=Octave.LINE1,
    )

    clef_f = Clef('clef2')
    assert clef_f.get_first_line_note() == Note(
        pitch=_Pitch(4),
        octave=Octave.GREAT,
    )
