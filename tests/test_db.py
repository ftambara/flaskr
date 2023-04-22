from sqlite3 import Connection

from flask import Flask
import pytest

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
def db_conn(app: Flask) -> Connection:
    # Make current_app available to db.get_db()
    with app.app_context():
        conn = db.get_db()
        conn.execute("CREATE TABLE test_table (test_field TEXT NOT NULL);")
        conn.execute("INSERT INTO test_table (test_field) VALUES ('test_value');")
        conn.commit()
        yield conn
        conn.execute("DROP TABLE test_table;")
        conn.commit()


class TestDB:
    def test_db_has_test_data(self, db_conn):
        result = db_conn.execute(
            "SELECT * FROM test_table WHERE test_field = 'test_value';"
        ).fetchone()
        assert result["test_field"] == "test_value"

    def test_can_insert_into_db(self, db_conn):
        item = {"test_field": "new_value"}
        db_conn.execute(
            "INSERT INTO test_table (test_field) VALUES (:test_field);", item
        )
        db_conn.commit()
        result = db_conn.execute(
            "SELECT * FROM test_table WHERE test_field = :test_field;", item
        ).fetchone()
        assert result["test_field"] == item["test_field"]

    def test_can_delete_from_db(self, db_conn):
        item = {"test_field": "new_value"}
        db_conn.execute(
            "INSERT INTO test_table (test_field) VALUES (:test_field);", item
        )
        db_conn.commit()
        db_conn.execute("DELETE FROM test_table WHERE test_field = :test_field;", item)
        db_conn.commit()
        result = db_conn.execute(
            "SELECT * FROM test_table WHERE test_field = :test_field;", item
        ).fetchone()
        assert result is None
