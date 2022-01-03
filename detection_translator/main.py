import argparse
import logging
from pathlib import Path

from detection_translator.common import NotationType
from detection_translator.session import DetectionTranslatorSession

logging.basicConfig(level=logging.INFO, format='%(asctime)s :: %(levelname)s :: %(message)s')


def _parse_args():
    parser = argparse.ArgumentParser(description='Args parser for detection-translator')
    parser.add_argument('--file_name', '-f', type=str, required=True,
                        help='file name without format (.png or .json) for image and exported data')
    parser.add_argument('--data_directory', '-d', type=str, required=True,
                        help='directory containing required files (detections json and image)')
    parser.add_argument('--output_directory', '-o', type=str, required=True,
                        help='directory containing required files (detections json and image)')

    args = parser.parse_args()
    print(args)
    return args


def main():
    args = _parse_args()

    data_directory = Path(args.data_directory)
    file = data_directory / f'exported_data_{args.file_name}.json'
    image = data_directory / f'{args.file_name}.png'
    logging.warning(f'Start processing "{image}" file')
    session = DetectionTranslatorSession(file, image, NotationType.FIFE_STAFF, args.output_directory)
    session.process()
    logging.warning(f'Done! File "{image}" processed successfully')


if __name__ == '__main__':
    main()
