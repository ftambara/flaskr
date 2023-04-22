from flask import Blueprint

bp = Blueprint('home', __name__, url_prefix='/')


@bp.get('/')
def index():
    return 'Hello, World!'
