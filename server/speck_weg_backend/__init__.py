# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: __init__.py
#

from flask import Flask, jsonify
from flask_jwt_extended import jwt_required
# Database migration: flask_migrate or alembic

from .config import Config
from .extensions import db, ma, hash_ctx, jwt, cors
from .routes import api_bp


def create_app(env: str = None):
    # instantiate the app
    app = Flask('speck_weg_backend')
    # Load the configuration
    # Todo: distinguish dev / test / prod
    app.config.from_object(Config(env))

    # Register all extensions to the application
    register_extensions(app)
    # Register all (nested) blueprints to  the application
    register_blueprints(app)

    # with app.app_context():
    # from . import routes, models  # noqa

    # Home route
    @app.route('/', methods=['GET'])
    def home():
        return 'Mis dihei isch dis dihei.', 200

    @app.route("/protected", methods=["GET", "POST"])
    @jwt_required()
    def protected():
        return jsonify(foo="bar")

    return app


def register_extensions(app: 'Flask'):
    """
    Register all external applications to the flask app

    :param app: Initialized Flask application
    :return: -
    """
    # SQLAlchemy with CRUD methods
    db.init_app(app)
    ma.init_app(app)
    # CryptContext for password hashing
    hash_ctx.init_app(app)
    # JWT
    jwt.init_app(app)
    # CORS
    cors.init_app(app)


def register_blueprints(app: 'Flask'):
    app.register_blueprint(api_bp)

