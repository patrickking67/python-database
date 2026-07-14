# Architecture

PeopleBase is a server-rendered Flask application with three layers kept intentionally close together for readability.

- `create_app()` owns configuration, database setup, and route registration.
- `Employee` defines the SQLAlchemy persistence model.
- Jinja templates and `static/styles.css` provide the interface.

SQLite is the zero-configuration default. `DATABASE_URL` can point SQLAlchemy at a production database without changing application code. Tests create an isolated SQLite database for every run.

The application is a portfolio and learning project, not a production HR system. A real deployment holding employee information also needs authentication, role-based authorization, CSRF protection, encryption, audit logging, backup policy, and data-retention controls.
