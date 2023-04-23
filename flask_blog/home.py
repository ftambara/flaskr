from flask import Blueprint, render_template

from .auth import login_required

bp = Blueprint("home", __name__, url_prefix="/")


@login_required
@bp.get("/")
def index():
    return render_template("home/index.html")
