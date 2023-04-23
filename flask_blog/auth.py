from typing import Callable
import functools

from flask import (
    Blueprint,
    flash,
    g,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug import Response
from werkzeug.security import check_password_hash, generate_password_hash

from flask_blog.db import get_db

bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route("/register", methods=("GET", "POST"))
def register() -> Response | str:
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None

        if not username:
            error = "Username is required."
        elif not password:
            error = "Password is required."
        elif (
            db.execute("SELECT id FROM user WHERE username = ?", (username,)).fetchone()
            is not None
        ):
            error = f"User {username} is already registered."

        if error:
            flash(error)
        else:
            db.execute(
                "INSERT INTO user (username, digest) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
            # Automatically log in the user after registering
            user = db.execute(
                "SELECT * FROM user WHERE username = ?", (username,)
            ).fetchone()
            login_user(user)
            return redirect(url_for("home.index"))

    return render_template("auth/register.html")


@bp.route("/login", methods=("GET", "POST"))
def login() -> Response | str:
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        db = get_db()
        error = None
        user = db.execute(
            "SELECT * FROM user WHERE username = ?", (username,)
        ).fetchone()

        if not user:
            error = "Incorrect username."
        elif not check_password_hash(user["digest"], password):
            error = "Incorrect password."

        if error:
            flash(error)
        else:
            login_user(user)
            return redirect(url_for("home.index"))

    return render_template("auth/login.html")


def login_user(user):
    session.clear()
    session["user_id"] = user["id"]


@bp.before_app_request
def load_logged_in_user() -> None:
    user_id = session.get("user_id")

    if not user_id:
        g.user = None
    else:
        g.user = (
            get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
        )


@bp.route("/logout")
def logout() -> Response:
    if "user_id" in session:
        del session["user_id"]
    return redirect(url_for("home.index"))


def login_required(view: Callable) -> Callable[..., Response]:
    @functools.wraps(view)
    def wrapped_view(**kwargs) -> Response:
        if not session.get("user_id"):
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view
