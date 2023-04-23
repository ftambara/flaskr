from flask.testing import FlaskClient


class TestHome:
    def test_index(self, client: FlaskClient) -> None:
        """
        GIVEN a Flask app
        WHEN the '/' page is requested (GET)
        THEN check the response is valid
        """
        response = client.get("/")
        assert b"Hello, World!" in response.data
