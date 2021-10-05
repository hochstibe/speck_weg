# speck_weg
# Stefan Hochuli, 04.10.2021,
# Folder: server/speck_weg_backend File: extensions.py
#

# from flask_cors import CORS
from flask_jwt_extended import JWTManager

from .database import CRUD
from .security import HashContext

# needs to be imported after SQLAlchemy (imported in CRUD)
from flask_marshmallow import Marshmallow


db = CRUD()
ma = Marshmallow()

hash_ctx = HashContext()
jwt = JWTManager()
# cors = CORS(resources={r'/*': {'origins': '*'}})
