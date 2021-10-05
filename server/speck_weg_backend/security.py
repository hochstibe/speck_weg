# speck_weg
# Stefan Hochuli, 05.10.2021,
# Folder: server/speck_weg_backend File: security.py
#

from typing import List

from passlib.context import CryptContext


class HashContext(CryptContext):

    def __init__(self, app=None, schemes: List[str] = ('argon2', 'pbkdf2_sha512')):
        super().__init__(schemes=schemes)

        self.app = app
        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        default_hash = app.config['DEFAULT_HASH']
        rounds = app.config['PW_ROUNDS']

        self.update(default=default_hash)
        self.update(argon2__default_rounds=rounds)
