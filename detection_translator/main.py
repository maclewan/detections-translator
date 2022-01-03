from pathlib import Path

from constants import DATA_PATH
from detection_translator.common import NotationType
from detection_translator_session import DetectionTranslatorSession


def main():
    file = Path(DATA_PATH) / 'exported_data_b2_116.json'
    image = Path(DATA_PATH) / 'b2_116.png'
    session = DetectionTranslatorSession(file, image, NotationType.FIFE_STAFF)
    session.process()


if __name__ == '__main__':
    main()
