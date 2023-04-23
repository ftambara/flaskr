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
    def test_blog_index(self, client, init_db):
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

    def test_a_logged_out_user_cannot_get_the_create_post_page(self, client, init_db):
        response = client.get("/create", follow_redirects=True)
        assert response.status_code == 200
        assert b"You must be logged in to view this page." in response.data

    def test_a_logged_in_user_can_get_the_create_post_page(
        self, client, logged_in_user
    ):
        response = client.get("/create", follow_redirects=True)
        assert response.status_code == 200
        assert b"Create a Post" in response.data

    def test_a_logged_out_user_cannot_create_a_post(self, client, init_db):
        response = client.post(
            "/create",
            data={"title": "title", "body": "body"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"You must be logged in to view this page." in response.data

    def test_a_logged_in_user_can_create_a_post(self, client, logged_in_user):
        response = client.post(
            "/create",
            data={"title": "title", "body": "body"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Post created!" in response.data
        assert b"title" in response.data
        assert b"body" in response.data
