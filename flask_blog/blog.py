from flask import (
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
