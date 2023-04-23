from flask import (
    abort,
    Blueprint,
    flash,
    g,
    render_template,
    redirect,
    request,
    Response,
    url_for,
)

from .auth import login_required
from .db import get_db

bp = Blueprint("blog", __name__, url_prefix="/")


@bp.get("/")
def index():
    g.posts = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username as author"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " ORDER BY created DESC"
            " LIMIT 10"
        )
        .fetchall()
    )
    return render_template("blog/index.html")


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create() -> Response | str:
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."
        elif not body:
            error = "Body is required."
        if error:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "INSERT INTO post (author_id, title, body) VALUES (?, ?, ?)",
                (g.user["id"], title, body),
            )
            db.commit()
            flash("Post created!")
            return redirect(url_for("blog.index"))

    return render_template("blog/create.html")


def get_post(post_id: int) -> dict[str, str]:
    post = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username as author"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE p.id = ?",
            (post_id,),
        )
        .fetchone()
    )

    if post is None:
        abort(404, f"Post id {post_id} doesn't exist.")

    return post


def get_user_posts(user_id: int) -> list[dict[str, str]]:
    # Check if user exists
    user = get_db().execute("SELECT * FROM user WHERE id = ?", (user_id,)).fetchone()
    if not user:
        abort(404, f"User id {user_id} doesn't exist.")

    posts = (
        get_db()
        .execute(
            "SELECT p.id, title, body, created, author_id, username as author"
            " FROM post p JOIN user u ON p.author_id = u.id"
            " WHERE author_id = ?"
            " ORDER BY created DESC",
            (user_id,),
        )
        .fetchall()
    )

    if not posts:
        abort(404, f"User id {user_id} has no posts.")

    return posts


@bp.route("/update/<int:post_id>", methods=("GET", "POST"))
@login_required
def update(post_id: int) -> Response | str:
    post = get_post(post_id)
    if post["author_id"] != g.user["id"]:
        abort(403)
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        error = None

        if not title:
            error = "Title is required."
        elif not body:
            error = "Body is required."
        if error:
            flash(error)
        else:
            db = get_db()
            db.execute(
                "UPDATE post SET title = ?, body = ? WHERE id = ?",
                (title, body, post_id),
            )
            db.commit()
            flash("Post updated!")
            return redirect(url_for("blog.index"))

    return render_template("blog/update.html", post=post)
