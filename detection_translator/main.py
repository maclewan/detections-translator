from pathlib import Path

from constants import DATA_PATH
from translator import Translator


def main():
    file = Path(DATA_PATH) / 'exported_data.json'
    image = Path(DATA_PATH) / 'b2_115.png'
    translator = Translator(file, image)
    translator.translate()


if __name__ == '__main__':
    main()
