from typing import List, Type

from detection_translator.common import NotationType
from detection_translator.feature_translator.base_feature_translator import BaseFeatureTranslator
from detection_translator.feature_translator.clef_translator import ClefTranslator
from detection_translator.feature_translator.note_translator import NoteTranslator


class FeatureTranslatorFactory:
    @staticmethod
    def get_translators(notation_type: NotationType) -> List[Type[BaseFeatureTranslator]]:
        if notation_type is NotationType.FIFE_STAFF:
            return [
                ClefTranslator,
                NoteTranslator,
                # SignTranslator,
            ]
        # elif notation_type is NotationType.MENSURAL:
        #     return []
        else:
            raise NotImplementedError(f'Notation type {notation_type} not implemented')

