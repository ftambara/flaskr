from sqlite3 import Connection

from flask import Flask

from flask_blog import db


class TestDB:
    def test_get_db(self, app: Flask) -> None:
        assert isinstance(db.get_db(), Connection)
        assert db.get_db() is db.get_db()

    def test_close_db(self, app: Flask) -> None:
        original_connection = db.get_db()
        db.close_db()
        assert db.get_db() is not original_connection

    def test_init_db(self, app: Flask) -> None:
        users_before_init = db.get_db().execute("SELECT * FROM user").fetchall()
        assert users_before_init
        db.init_db()
        users_after_init = db.get_db().execute("SELECT * FROM user").fetchall()
        assert not users_after_init
