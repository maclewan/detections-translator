from pathlib import Path

from constants import DATA_PATH
from translator import Translator


def main():
    file = Path(DATA_PATH) / 'exported_data.json'
    translator = Translator(file)
    translator.translate()


if __name__ == '__main__':
    main()
