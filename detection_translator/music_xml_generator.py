from typing import List, Union

from detection_translator.bar import Bar
from detection_translator.common import SubStaff
from detection_translator.staff import Staff
from detection_translator.note import Note as DetectionNote
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

        if len(sections) == 0:
            return None, None

        notes_soprano = []
        notes_alto = []
        notes_tenor = []
        notes_bass = []
        for section in sections:
            top_section, bottom_section = section[0], section[1]
            if len(top_section) == 2:
                notes_soprano.append(top_section[0])
                notes_alto.append(top_section[1])

            if len(bottom_section) == 2:
                notes_tenor.append(bottom_section[0])
                notes_bass.append(bottom_section[1])

        return (Measure([notes_soprano, notes_alto], time_signature=(100, 4), clef='treble'),
                Measure([notes_tenor, notes_bass], time_signature=(100, 4), clef='bass'))

    @staticmethod
    def _get_section(section: List[DetectionNote]) -> List[List[Union[Note, Rest]]]:

        top_notes = [
            (Note(n.xml_name, 1) if isinstance(n, DetectionNote) else Rest(duration=n.duration)) for n in section if n.sub_staff is SubStaff.TOP
        ]
        bottom_notes = [
            (Note(n.xml_name, 1) if isinstance(n, DetectionNote) else Rest(duration=n.duration)) for n in section if n.sub_staff is SubStaff.BOTTOM
        ]
        if len(top_notes) == 1:
            top_notes.append(Rest(1.0))
        if len(bottom_notes) == 1:
            bottom_notes.append(Rest(1.0))

        top_section = top_notes if top_notes else [Rest(1.0), Rest(1.0)]
        bottom_section = bottom_notes if bottom_notes else [Rest(1.0), Rest(1.0)]

        return [top_section, bottom_section]
