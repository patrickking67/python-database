# PeopleBase

A focused Flask and SQLAlchemy application for managing structured employee records.

## What it demonstrates

- Application-factory architecture and environment-based configuration
- Create, read, update, and delete workflows
- Server-side validation with useful error states
- POST-only destructive actions
- Responsive, accessible server-rendered templates
- Isolated integration tests across supported Python versions

## Run locally

```bash
git clone https://github.com/patrickking67/python-database.git
cd python-database
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
flask --app app run --debug
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000). The SQLite database is created under `instance/` and is ignored by Git.

## Verify

```bash
pytest -q
python scripts/check-ai-config.py
```

## Configuration

| Variable | Purpose | Default |
| --- | --- | --- |
| `DATABASE_URL` | SQLAlchemy database connection | Local SQLite |
| `SECRET_KEY` | Session and flash-message signing | Development-only value |
| `FLASK_DEBUG` | Enables debug mode when set to `1` | Disabled |

Set a unique `SECRET_KEY` and add authentication before any public deployment. See [architecture](docs/architecture.md) and [security policy](SECURITY.md).

## License

MIT © Patrick King
