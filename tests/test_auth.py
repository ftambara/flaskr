class TestAuth:
    register_url = "/auth/register"
    login_url = "/auth/login"
    logout_url = "/auth/logout"

    def test_can_get_register_page(self, client):
        response = client.get(self.register_url)
        assert response.status_code == 200

    def test_can_register(self, client):
        response = client.post(
            self.register_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Flaskr" in response.data

    def test_newly_registered_user_is_logged_in(self, client):
        response = client.post(
            self.register_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"username" in response.data

    def test_cannot_register_without_username(self, client):
        response = client.post(
            self.register_url,
            data={"username": "", "password": "password"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Username is required." in response.data

    def test_cannot_register_without_password(self, client):
        response = client.post(
            self.register_url,
            data={"username": "username", "password": ""},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"Password is required." in response.data

    def test_cannot_register_with_existing_username(self, client):
        client.post(
            self.register_url,
            data={"username": "existing", "password": "password"},
            follow_redirects=True,
        )
        response = client.post(
            self.register_url,
            data={"username": "existing", "password": "password"},
            follow_redirects=True,
        )
        assert response.status_code == 200
        assert b"already registered" in response.data

    def test_can_get_login_page(self, client):
        response = client.get(self.login_url)
        assert response.status_code == 200

    def test_a_registered_user_can_login(self, client):
        client.post(
            self.register_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        response = client.post(
            self.login_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        assert response.status_code == 200

    def test_a_registered_user_can_logout(self, client):
        client.post(
            self.register_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        client.post(
            self.login_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        response = client.get(self.logout_url, follow_redirects=True)
        assert response.status_code == 200

    def test_a_logged_in_user_can_access_the_index_page(self, client):
        client.post(
            self.register_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        client.post(
            self.login_url,
            data={"username": "username", "password": "password"},
            follow_redirects=True,
        )
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200

    def test_a_logged_out_user_can_access_the_login_page(self, client):
        response = client.get(self.login_url, follow_redirects=True)
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_a_logged_out_user_cannot_access_the_index_page(self, client):
        response = client.get("/", follow_redirects=True)
        assert response.status_code == 200
        assert b"Log In" in response.data

    def test_a_logged_out_user_can_access_the_register_page(self, client):
        response = client.get(self.register_url, follow_redirects=True)
        assert response.status_code == 200
        assert b"Register" in response.data

    def test_a_logged_out_user_can_access_the_logout_page(self, client):
        response = client.get(self.logout_url, follow_redirects=True)
        assert response.status_code == 200
