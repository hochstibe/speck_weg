# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: __init__.py
#

from flask import Flask
# Database migration: flask_migrate or alembic

from .config import Config
from .database import CRUD
from .app.speck_weg import SpeckWeg

# instantiate the app
app = Flask('speck_weg_backend')
# Load the configuration
# Todo: distinguish dev / test / prod
app.config.from_object(Config)

# Set the database
db = CRUD(app)

# enable CORS
# CORS(app, resources={r'/*': {'origins': '*'}})

# Use the instance of the class SpeckWeg as the global application
speck_weg = SpeckWeg()

# get routes / models
with app.app_context():
    from . import routes, models  # noqa
