import pytest

from flask_blog.blog import get_post


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


@pytest.fixture
def created_post(client, registered_user):
    # Log in the user
    client.post(
        "/auth/login",
        data=registered_user,
        follow_redirects=True,
    )
    # Create a post
    post = {"title": "title", "body": "body"}
    client.post(
        "/create",
        data=post,
        follow_redirects=True,
    )
    # Log out the user, so the only effect of this fixture is to create a post
    client.get("/auth/logout", follow_redirects=True)
    return get_post(1)


class TestBlog:
    def test_blog_index(self, client, created_post):
        response = client.get("/")
        assert response.status_code == 200
        assert b"Latest Posts" in response.data
        assert b"title" in response.data
        assert b"body" in response.data

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

    def test_a_logged_out_user_cannot_get_the_update_post_page(
        self, client, created_post
    ):
        response = client.get(f"/update/{created_post['id']}", follow_redirects=True)
        assert response.status_code == 200
        assert b"You must be logged in to view this page." in response.data

    def test_a_logged_in_user_can_get_the_update_post_page_for_its_own_post(
        self, client, logged_in_user
    ):
        client.post(
            "/create",
            data={"title": "title", "body": "body"},
            follow_redirects=True,
        )
        response = client.get("/update/1", follow_redirects=True)
        assert response.status_code == 200
        assert b"Update Post" in response.data

    def test_a_logged_in_user_cannot_get_the_update_post_page_for_another_users_post(
        self, client, created_post
    ):
        # Register another user, log in should be done automatically
        client.post(
            "/auth/register",
            data={"username": "username2", "password": "password"},
            follow_redirects=True,
        )
        response = client.get("/update/1", follow_redirects=True)
        assert response.status_code == 403

    def test_a_logged_out_user_cannot_update_a_post(self, client, created_post):
        response = client.post(
            f"/update/{created_post['id']}",
            data={"title": "title", "body": "body"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"You must be logged in to view this page." in response.data

    def test_a_logged_in_user_cannot_update_another_users_post(
        self, client, created_post
    ):
        # Register another user, log in should be done automatically
        client.post(
            "/auth/register",
            data={"username": "username2", "password": "password"},
            follow_redirects=True,
        )
        response = client.post(
            f"/update/{created_post['id']}",
            data={"title": "title", "body": "body"},
            follow_redirects=True,
        )
        assert response.status_code == 403

    # Note: `created_post` must be before `logged_in_user` because `created_post`
    # logs out the user.
    def test_a_logged_in_user_can_update_its_own_post(
        self, client, created_post, logged_in_user
    ):
        response = client.post(
            f"/update/{created_post['id']}",
            data={"title": "title", "body": "body"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Post updated!" in response.data
        assert b"title" in response.data
        assert b"body" in response.data

    def test_a_logged_out_user_cannot_delete_a_post(self, client, created_post):
        response = client.post(f"/delete/{created_post['id']}", follow_redirects=True)
        assert response.status_code == 200
        assert b"You must be logged in to view this page." in response.data

    def test_a_logged_in_user_cannot_delete_another_users_post(
        self, client, created_post
    ):
        # Register another user, log in should be done automatically
        client.post(
            "/auth/register",
            data={"username": "username2", "password": "password"},
            follow_redirects=True,
        )
        response = client.post(f"/delete/{created_post['id']}", follow_redirects=True)
        assert response.status_code == 403

    # Note: `created_post` must be before `logged_in_user` because `created_post`
    # logs out the user.
    def test_a_logged_in_user_can_delete_its_own_post(
        self, client, created_post, logged_in_user
    ):
        response = client.post(f"/delete/{created_post['id']}", follow_redirects=True)
        assert response.status_code == 200
        assert b"Post deleted!" in response.data
