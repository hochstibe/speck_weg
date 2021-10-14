# speck_weg
# Stefan Hochuli, 04.10.2021,
# Folder: server/database File: __init__.py
#


from typing import List, Union, Any, Type, TYPE_CHECKING

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import select, MetaData


if TYPE_CHECKING:
    from sqlalchemy.orm import DeclarativeMeta
    from flask import Flask


metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_N_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
)


class CRUD(SQLAlchemy):

    def __init__(self, app: 'Flask' = None, drop_all=False):

        super().__init__(app=app, metadata=metadata)

        if drop_all:
            self.metadata.drop_all(self.engine)
            self.metadata.create_all(self.engine)

    def create(self, obj: Union[List, 'DeclarativeMeta']):

        try:
            if isinstance(obj, list):
                self.session.add_all(obj)
            else:
                self.session.add(obj)
            self.session.commit()
        except Exception as exc:
            print(exc)
            self.session.rollback()
            raise exc

    def read_first(self, stmt) -> Any:

        try:
            res = self.session.execute(stmt).scalars().first()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read_one(self, stmt, unique=False) -> Any:
        # unique: if joinedload for a collection uf children -> matches them uniquely
        # error, if it cant find the tuple
        try:
            if unique:
                res = self.session.execute(stmt).scalars().unique().one()
            else:
                res = self.session.execute(stmt).scalars().one()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read_all(self, cls: Type['DeclarativeMeta']) -> List[Any]:

        stmt = select(cls)

        # without scalars --> rows with lists of obj
        try:
            res = self.session.execute(stmt).scalars().all()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def read_stmt(self, stmt, unique=False):
        # unique: if joinedload for a collection uf children -> matches them uniquely
        try:
            if unique:
                res = self.session.execute(stmt).scalars().unique().all()
            else:
                res = self.session.execute(stmt).scalars().all()
        except Exception as exc:
            print(exc)
            raise exc

        return res

    def update(self, stmt=None, payload=None):
        # commit recent changes
        if stmt is not None:
            # Only for updates via sqlalchemy core
            # If an ORM-Model is changed, it will update with the commit
            self.session.execute(stmt, payload)
        self.session.commit()

    def delete_stmt(self, stmt):

        try:
            self.session.execute(stmt)
            self.session.commit()

        except Exception as exc:
            print(exc)
            raise exc

    def delete(self, obj: Union[List, 'DeclarativeMeta'] = None):

        try:
            if isinstance(obj, (list, tuple)):
                for o in obj:
                    self.session.delete(o)
            else:
                self.session.delete(obj)
            self.session.commit()

        except Exception as exc:
            print(exc)
            raise exc
