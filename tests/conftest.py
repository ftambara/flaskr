import pytest
from flask import Flask
from flask.testing import FlaskClient

from flask_blog import create_app, db


@pytest.fixture
def app() -> Flask:
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": ":memory:",
        }
    )
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    A test client for the app.
    :param app: The Flask app.
    :return: A Flask test client.
    """
    return app.test_client()


@pytest.fixture
def init_db(app: Flask) -> None:
    """
    Initialize the database.
    :param app: The Flask app.
    """
    with app.app_context():
        db.init_db()
        yield
