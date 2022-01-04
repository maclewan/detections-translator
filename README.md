# Base setup

```bash
python3 -m venv .venv
pip install -r requiremenets.txt
```

# Tests
Run tests and coverage:
```bash
pytest --cov-report term-missing --cov detection_translator test
```
Exclude integration test:
```bash
pytest --cov-report term-missing --cov detection_translator test --ignore=test/test_integration.py 
```