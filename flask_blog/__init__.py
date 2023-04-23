import os

from flask import Flask


def create_app(test_config=None):
    """
    Create and configure an instance of the Flask application.
    :return: The Flask app.
    """
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="dev",
        DATABASE=os.path.join(app.instance_path, "a-store.sqlite"),
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)

    # Create instance folder if it does not exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # Register the routes
    from . import home

    app.register_blueprint(home.bp)

    # Register the auth blueprint
    from . import auth

    app.register_blueprint(auth.bp)

    # Register the database
    from . import db

    db.init_app(app)

    return app
