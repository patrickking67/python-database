import pytest

from app import Employee, create_app, db


@pytest.fixture()
def app(tmp_path):
    application = create_app(
        {
            "TESTING": True,
            "SECRET_KEY": "test",
            "SQLALCHEMY_DATABASE_URI": f"sqlite:///{tmp_path / 'test.db'}",
        }
    )

    with application.app_context():
        db.session.add(Employee(name="Ada Lovelace", position="Engineer", salary=125000))
        db.session.commit()

    yield application

    with application.app_context():
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()
