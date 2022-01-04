from pathlib import Path
import os
from detection_translator.main import main_wrapper


def test_integration():
    data_path = Path(__file__).parent.resolve() / 'data'
    main_wrapper(output_directory=data_path, file=data_path / 'test.json', image=data_path / 'test.png')
    assert (data_path / 'reference.musicxml').read_text() == (data_path / 'test_staff0.musicxml').read_text()
