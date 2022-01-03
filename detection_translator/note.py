from dataclasses import dataclass
from enum import Enum
from typing import Tuple

from detection_translator.common import SubStaff


PITCH_NAMES_MAP = {
    0: 'c',
    1: 'd',
    2: 'e',
    3: 'f',
    4: 'g',
    5: 'a',
    6: 'b',
}



class _Pitch(Enum):
    C = 0
    D = 1
    E = 2
    F = 3
    G = 4
    A = 5
    H = 6


    def plus(self, setps: int) -> Tuple['_Pitch', int]:
        """
        :param setps: tones to add (can be negative)
        :return: new Pitch and octave difference
        """
        new_pitch = (self.value + setps) % 7
        octaves = (self.value + setps) // 7
        return _Pitch(new_pitch), octaves


class Alteration(Enum):
    SHARP = 0
    FLAT = 1
    NATURAL = 2

    @property
    def xml_sign(self):
        if self is Alteration.SHARP:
            return '#'
        elif self is Alteration.FLAT:
            return 'b'
        else:
            return ''


class Octave(Enum):
    CONTRA = 1
    GREAT = 2
    SMALL = 3
    LINE1 = 4
    LINE2 = 5
    LINE3 = 6
    LINE4 = 7


class Head(Enum):
    HEAD_FULL = 0
    HEAD_EMPTY = 1


@dataclass
class Note:
    pitch: _Pitch
    octave: Octave
    head: Head = None
    alteration: Alteration = None
    sub_staff: SubStaff = None

    def plus(self, steps: int) -> 'Note':
        new_pitch, octave_shift = self.pitch.plus(steps)
        return Note(
            new_pitch,
            Octave(self.octave.value + octave_shift),
            alteration=Alteration.NATURAL,
        )

    @property
    def xml_name(self):
        return f'{PITCH_NAMES_MAP[self.pitch.value]}{self.alteration.xml_sign}{self.octave.value}'


@dataclass
class Rest:
    sub_staff: SubStaff
    duration: float = 1
