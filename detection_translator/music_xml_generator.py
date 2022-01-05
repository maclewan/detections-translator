from time import sleep
from typing import List, Union, Tuple

from detection_translator.bar import Bar
from detection_translator.common import SubStaff, Point
from detection_translator.staff import Staff
from detection_translator.note import Note as DetectionNote, Direction
from pymusicxml import Score, PartGroup, Part, Measure, Note, Rest


class MusicXmlGenerator:  # pragma: no cover
    _staff: Staff

    def __init__(self, staff: Staff):
        self._staff = staff

    def generate(self, name: str):
        top_bar_notes = [
            bar_notes for bar in self._staff.bars if (bar_notes := self._get_bar(bar)[0]) is not None
        ]
        bottom_bar_notes = [
            bar_notes for bar in self._staff.bars if (bar_notes := self._get_bar(bar)[1]) is not None
        ]
        score = Score([
            PartGroup([
                Part("Top", top_bar_notes),
                Part("Bottom", bottom_bar_notes)
            ]),

        ], title=name, composer="detections-translator")
        score.export_to_file(f"{name}.musicxml")

    def _get_bar(self, bar: Bar):
        sections = [self._get_section(s) for s in bar.sections]
        notes_soprano, notes_alto, notes_tenor, notes_bass = self._resolve_sections(sections)

        return (Measure([notes_soprano, notes_alto], time_signature=(100, 4), clef='treble'),
                Measure([notes_tenor, notes_bass], time_signature=(100, 4), clef='bass'))

    @staticmethod
    def _resolve_sections(sections: List[List[List[Tuple[Union[Note, Rest], DetectionNote]]]]):
        notes_soprano = []
        notes_alto = []
        notes_tenor = []
        notes_bass = []

        # Directions first
        for section in sections:
            top_notes: List[Tuple[Union[Note, Rest], DetectionNote]]
            bottom_notes: List[Tuple[Union[Note, Rest], DetectionNote]]
            top_notes, bottom_notes = section

            def handle_section(notes):
                higher = []
                lower = []
                if len(notes) == 2:  # easy case
                    first, det1 = notes[0]
                    second, det2 = notes[1]
                    dir1, dir2 = det1.direction, det2.direction

                    if dir1 is None and dir2 is None:
                        dir1 = Direction.UP
                        dir2 = Direction.DOWN
                    if dir1 is None:
                        dir2 = Direction.DOWN if dir1 is Direction.UP else Direction.DOWN
                    if dir2 is None:
                        dir1 = Direction.DOWN if dir2 is Direction.UP else Direction.DOWN

                    higher.append(first if dir1 is Direction.UP else second)
                    lower.append(first if dir1 is Direction.DOWN else second)

                elif len(notes) == 1:
                    first, det1 = notes[0]
                    dir1 = det1.direction

                    if dir1 is None:
                        dir1 = input_direction(det1.center)
                    if dir1 is Direction.DOWN:
                        lower.append(first)
                    else:
                        higher.append(first)

                return higher, lower

            higher, lower = handle_section(top_notes)
            notes_soprano.extend(higher)
            notes_alto.extend(lower)

            higher, lower = handle_section(bottom_notes)
            notes_tenor.extend(higher)
            notes_bass.extend(lower)

        voices = [notes_soprano, notes_alto, notes_tenor, notes_bass]


        return notes_soprano, notes_alto, notes_tenor, notes_bass

    @staticmethod
    def _get_section(raw_section: List[DetectionNote]) -> List[List[Tuple[Union[Note, Rest], DetectionNote]]]:
        for note in raw_section:
            if note.duration is None:
                note.duration = input_length(note.center)

        raw_section.sort(key=lambda d: d.center.y)

        top_notes = [
            ((Note(n.xml_name, n.duration), n) if isinstance(n, DetectionNote)
             else (Rest(duration=n.duration), None))
            for n in raw_section if n.sub_staff is SubStaff.TOP
        ]
        bottom_notes = [
            ((Note(n.xml_name, n.duration), n) if isinstance(n, DetectionNote)
             else (Rest(duration=n.duration), None))
            for n in raw_section if n.sub_staff is SubStaff.BOTTOM
        ]
        # if len(top_notes) == 1:
        #     top_notes.append(Rest(1.0))
        # if len(bottom_notes) == 1:
        #     bottom_notes.append(Rest(1.0))

        return [top_notes, bottom_notes]


def input_direction(coords: Point) -> Direction:
    sleep(0.1)
    a = input(f'Is note on {coords} direction UP? (Y/N): ')
    return Direction.UP if a.upper() == 'Y' else Direction.DOWN


def input_length(coords: Point) -> float:
    sleep(0.1)
    try:
        return float(input(f'Input note on {coords} length (1: quarter, 0.5: eight, ect): '))
    except ValueError:
        print('Wrong value, assuming quarter')
        return 1.0
