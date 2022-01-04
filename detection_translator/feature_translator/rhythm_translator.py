import logging
from typing import List

from detection_translator.bar import Bar
from detection_translator.constants import NOTE_CLASSES, HEAD_AREA_MARGIN, RHYTHM_CLASSES, CLASSES_TO_DURATION
from detection_translator.detection import DetectionData, Detection
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.note import Note, Rest, Head, Direction
from detection_translator.staff import Staff


class RhythmTranslator(BaseFeatureTranslator):

    def __init__(self, staffs: List[Staff], detection_data: DetectionData):
        translator_classes = [k for k, v in detection_data.category_index.items() if v in RHYTHM_CLASSES]
        super().__init__(staffs, detection_data, translator_classes)

    def _translate(self, staff: Staff):
        detections = [d for d in self._filtered_detections if d.staff_id == staff.index]

        for bar in staff.bars:
            bar_rhythms = [d for d in detections if d in bar]
            for section in bar.sections:
                for note in section:
                    if note.duration is not None and note.direction is not None:
                        continue
                    rhythm_candidates = [r for r in bar_rhythms if
                                         r.contains(y=note.center.y, x=note.center.x,
                                                    margin=0)]  # todo: maybe negativa value
                    rhythm_candidates.sort(key=lambda r: abs(r.center.x - note.center.x))
                    if len(rhythm_candidates) > 1 and len(section) < 4:
                        c1, c2 = rhythm_candidates[0], rhythm_candidates[1]
                        if (c1.det_class != c2.det_class
                                or note.check_rhythm_direction(c1) == note.check_rhythm_direction(c2)):
                            rhythm_candidates = rhythm_candidates[:1]
                        else:
                            duration = self._translate_note_duration(note.head, rhythm_candidates[0])
                            note.duration = duration
                            note_copy = note.copy()
                            note.direction = Direction.UP
                            note_copy.direction = Direction.DOWN
                            section.append(note_copy)

                    if len(rhythm_candidates) == 1:
                        direction = note.check_rhythm_direction(rhythm_candidates[0])
                        duration = self._translate_note_duration(note.head, rhythm_candidates[0])
                        note.direction = direction
                        note.duration = duration

    @staticmethod
    def _translate_note_duration(head: Head, rhythm: Detection) -> float:
        if head is Head.HEAD_EMPTY:
            if 'dot' in rhythm.det_class:
                return 3.0
            else:
                return 2.0
        if head is Head.HEAD_FULL:
            return CLASSES_TO_DURATION[rhythm.det_class]
