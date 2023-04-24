import os

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
            # "DATABASE": db_path,
        }
    )
    data_path = os.path.join(os.path.dirname(__file__), "data.sql")
    with open(data_path, "rb") as f:
        data_sql = f.read().decode("utf8")

    with app.app_context():
        db.init_db()
        db.get_db().executescript(data_sql)
        yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    A test client for the app.
    :param app: The Flask app.
    :return: A Flask test client.
    """
    return app.test_client()
