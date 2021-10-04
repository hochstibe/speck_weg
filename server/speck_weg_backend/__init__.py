# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: __init__.py
#

from flask import Flask
# Database migration: flask_migrate or alembic

from .config import Config
from .extensions import db


def register_extensions(app: 'Flask'):
    """
    Register all external applications to the flask app

    :param app: Initialized Flask application
    :return: -
    """
    db.init_app(app)


def create_app():
    # instantiate the app
    app = Flask('speck_weg_backend')
    # Load the configuration
    # Todo: distinguish dev / test / prod
    app.config.from_object(Config)

    register_extensions(app)

    # Use the instance of the class SpeckWeg as the global application
    # Probably not possible --> related to the session of the logged-in user
    # speck_weg = SpeckWeg()

    # get routes / models
    with app.app_context():
        from . import routes, models  # noqa

    return app
