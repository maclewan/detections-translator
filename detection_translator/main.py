from pathlib import Path

from constants import DATA_PATH
from session_processor import SessionProcessor


def main():
    file = Path(DATA_PATH) / 'exported_data.json'
    image = Path(DATA_PATH) / 'b2_115.png'
    processor = SessionProcessor(file, image)
    processor.process()


if __name__ == '__main__':
    main()
