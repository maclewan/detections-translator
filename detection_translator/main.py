import argparse
from pathlib import Path

from constants import DATA_PATH
from detection_translator.common import NotationType
from detection_translator_session import DetectionTranslatorSession


def _parse_args():
    parser = argparse.ArgumentParser(description='Args parser for detection-translator')
    parser.add_argument('file name', type=str, help='file name without format (.png or .json) for image and exported data')
    args = parser.parse_args()
    return args


def main(args):
    file = Path(DATA_PATH) / f'exported_data_{args.name}.json'
    image = Path(DATA_PATH) / f'{args.name}.png'
    session = DetectionTranslatorSession(file, image, NotationType.FIFE_STAFF)
    session.process()


if __name__ == '__main__':
    parsed_args = _parse_args()
    main(parsed_args)
