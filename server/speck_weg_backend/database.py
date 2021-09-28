# speck_weg
# Stefan Hochuli, 27.09.2021,
# Folder: server/speck_weg_backend File: database.py
#

from sqlalchemy import MetaData, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import load_db_config


# Skip flask-sqlalchemy (use plain sqlalchemy)
# httpas://towardsdatascience.com/use-flask-and-sqlalchemy-not-flask-sqlalchemy-5a64fafe22a4
config = load_db_config()

# if 'sqlite' in config['DATABASE_CONNECTION_URI']:
#     engine = create_engine(config['DATABASE_CONNECTION_URI'],
#                            connect_args={'check_same_thread': False})

engine = create_engine(config['DATABASE_CONNECTION_URI'], echo=True, future=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_N_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)
Base = declarative_base(metadata=metadata)


# Use the database without flask: (see towardsdatascience)
def get_db_session(echo: bool = True, drop_all=False) -> 'sessionmaker':

    engine.echo = echo
    if drop_all:
        metadata.drop_all(engine)
    metadata.create_all(engine)

    return SessionLocal
