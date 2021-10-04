# speck_weg
# Stefan Hochuli, 04.10.2021,
# Folder: server/speck_weg_backend File: extensions.py
#

# from flask_cors import CORS

from .database import CRUD

db = CRUD()
# cors = CORS(resources={r'/*': {'origins': '*'}})
