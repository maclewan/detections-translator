from typing import List

from detection_translator.bar import Bar
from detection_translator.constants import NOTE_CLASSES, HEAD_AREA_MARGIN
from detection_translator.detection import DetectionData, Detection
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.note import Note
from detection_translator.staff import Staff


class NoteTranslator(BaseFeatureTranslator):

    def __init__(self, staffs: List[Staff], detection_data: DetectionData):
        translator_classes = [k for k, v in detection_data.category_index.items() if v in NOTE_CLASSES]
        super().__init__(staffs, detection_data, translator_classes)

    def _translate(self, staff: Staff):
        detections = [d for d in self._filtered_detections if d.staff_id == staff.index]

        for bar in staff.bars:
            sections = self._generate_sections(bar, detections)
            sections_translated = [[self._translate_detection(detection, bar) for detection in section] for section in sections]
            bar.sections = sections_translated

    @staticmethod
    def _generate_sections(bar: Bar, detections: List[Detection]):
        bar_notes = [d for d in detections if d in bar]
        bar_notes.sort(key=lambda d: d.center.y)

        sections = []
        for note in bar_notes:
            if not ((bar.line_distance ** 2) * HEAD_AREA_MARGIN > note.height * note.width):
                print('Is it note?', note, 'Skipping...')
                continue
            if not sections:
                sections.append([note])
                continue
            for section in sections[::-1]:

                for section_note in section:
                    if (section_note.contains(x=note.center.x) or
                            (section_note.contains(y=note.center.y, margin=bar.line_distance // 3) and
                             section_note.contains(x=note.center.x, margin=(bar.line_distance * 3 // 4)))):
                        section.append(note)
                        break
                else:
                    continue
                break
            else:
                sections.append([note])
                continue

        sections_sorted = sorted(sections, key=lambda s: s[0].center.x)
        sections_sorted = [sorted(ss, key=lambda s: s.center.y) for ss in sections_sorted]
        return sections_sorted

    @staticmethod
    def _translate_detection(detection: Detection, bar: Bar) -> Note:
        line, sub_staff = bar.get_location(detection)

        staff_first_note = bar.clefs[sub_staff].get_first_line_note()
        note = staff_first_note.plus(line*2)
        note.sub_staff = sub_staff
        return note
