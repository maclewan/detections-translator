# Base setup

```bash
python3 -m venv .venv
pip install -r requiremenets.txt
```

# Tests
Run tests and coverage:
```bash
pytest --cov detection_translator test/
pytest --cov-report term-missing --cov detection_translator test
```