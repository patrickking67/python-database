# Repository instructions

PeopleBase is a focused Flask and SQLAlchemy CRUD application. Keep the application factory in `app.py`, preserve POST-only deletion, validate all submitted employee data, and add tests for behavior changes.

## Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pytest -q
python scripts/check-ai-config.py
```

Do not commit databases, virtual environments, environment files, user-local agent state, or credentials.
