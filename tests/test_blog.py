class TestBlog:
    def test_blog_index(self, client):
        response = client.get("/blog/")
        assert response.status_code == 200
        assert b"Latest Posts" in response.data
