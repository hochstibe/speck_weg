# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: user.py
#

from typing import Optional, Union

from sqlalchemy import select

from ..extensions import db
from ..models import UserModel


class User:
    def __init__(self, usr_id: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.model: Optional['UserModel'] = None

        # initially search for the current user (if not given)
        if usr_id:
            stmt = select(UserModel).where(UserModel.usr_id == usr_id)
            res = db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        if not usr_id:
            self.model = self.read_current_user()

    @staticmethod
    def read_current_user() -> Union['UserModel', None]:
        # selects the first entry in the user table
        stmt = select(UserModel)
        return db.read_first(stmt)

    def update_usr_attributes(self, name: str, weight: float):
        # update all attributes

        self.model.name = name
        self.model.weight = weight

    def save_user(self, name: str, weight: float):
        if self.model:
            self.update_usr_attributes(name, weight)
            db.update()

        else:
            self.model = UserModel()
            self.update_usr_attributes(name, weight)
            db.create(self.model)
