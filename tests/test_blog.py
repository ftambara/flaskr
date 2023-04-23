import pytest


@pytest.fixture
def user():
    return {"username": "username", "password": "password"}


@pytest.fixture
def registered_user(client, init_db, user):
    client.post(
        "/auth/register",
        data=user,
        follow_redirects=True,
    )
    return user


@pytest.fixture
def logged_in_user(client, registered_user):
    client.post(
        "/auth/login",
        data=registered_user,
        follow_redirects=True,
    )
    return registered_user


class TestBlog:
    def test_blog_index(self, client):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Latest Posts" in response.data

    def test_a_logged_out_user_can_access_the_blog_index_page(self, client, init_db):
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Latest Posts" in response.data

    def test_a_logged_in_user_can_access_the_blog_index_page(
        self, client, init_db, logged_in_user
    ):
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Latest Posts" in response.data
