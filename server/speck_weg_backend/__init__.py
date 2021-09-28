# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: __init__.py
#

from flask import Flask, jsonify, _app_ctx_stack
from flask_sqlalchemy import SQLAlchemy
# Database migration: flask_migrate or alembic

from .config import Config

# instantiate the app
app = Flask('speck_weg_backend')
app.config.from_object(Config)
print(app.config)
db = SQLAlchemy(app)

# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})

# get routes / models
with app.app_context():
    from . import routes, models  # noqa
