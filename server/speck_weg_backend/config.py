# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: config.py
#

import os

from pathlib import Path

from environs import Env


class Config:

    env = Env()

    folder = Path.cwd()

    # cwd to /speck_weg/
    for i, name in enumerate(folder.parts):
        if name == 'speck_weg':
            # currently in a subdirectory
            for j in range(len(folder.parts) - i - 1):
                folder = folder.parent

    folder = folder / 'instance'
    file = folder / '.env.dev'
    env.read_env(file)

    # Get the configuration from the environment

    # Develop mode
    ENV = env.str('FLASK_ENV', default='development')

    # DB
    user = env.str('POSTGRES_USER')
    password = env.str('POSTGRES_PASSWORD')
    host = env.str('POSTGRES_HOST')
    port = env.str('POSTGRES_PORT')
    database = env.str('POSTGRES_DB')
    SQLALCHEMY_DATABASE_URI = f'postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Security
    # Hashing rounds
    DEFAULT_HASH = env.str('DEFAULT_HASH')
    PW_ROUNDS = env.int('PW_ROUNDS')
    # JWT
    JWT_SECRET_KEY = env.str('JWT_SECRET_KEY')

    def __init__(self, env: str = None):
        # Only used for the testing environment at the moment
        if env:
            if env == 'testing':
                self.TESTING = True
