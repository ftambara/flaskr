import pytest
from flask import Flask
from flask.testing import FlaskClient

from flask_blog import create_app


@pytest.fixture
def app() -> Flask:
    """
    Create and configure a new app instance for each test.
    :return: The Flask app.
    """
    app = create_app({'TESTING': True})
    yield app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """
    A test client for the app.
    :param app: The Flask app.
    :return: A Flask test client.
    """
    return app.test_client()


class TestHome:
    def test_index(self, client: FlaskClient) -> None:
        """
        GIVEN a Flask app
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
        """
        response = client.get('/')
        assert b'Hello, World!' in response.data
