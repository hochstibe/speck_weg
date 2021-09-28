# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: backend_app.py
#

from flask import Flask, jsonify, _app_ctx_stack
from sqlalchemy.orm import scoped_session

from .database import get_db_session


def create_app(mode: str):

    # instantiate the app
    app = Flask('speck_weg_backend')

    if mode == 'dev':
        app.config.from_object('speck_weg_backend.config')
    print(app.config)

    # enable CORS
    # CORS(app, resources={r'/*': {'origins': '*'}})

    # set up the database
    with app.app_context():
        SessionLocal = get_db_session(echo=True, drop_all=False)
        app.db_session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

        from . import routes  # noqa

    return app
