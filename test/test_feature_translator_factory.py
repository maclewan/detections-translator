from detection_translator.common import NotationType
from detection_translator.feature_translator.clef_translator import ClefTranslator
from detection_translator.feature_translator.feature_translator_factory import FeatureTranslatorFactory
from detection_translator.feature_translator.note_translator import NoteTranslator
from detection_translator.feature_translator.rhythm_translator import RhythmTranslator


def test_translator_factory():
    assert FeatureTranslatorFactory.get_translators(NotationType.FIFE_STAFF) == [
        ClefTranslator,
        NoteTranslator,
        RhythmTranslator,
    ]
