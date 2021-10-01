# speck_weg
# Stefan Hochuli, 30.09.2021,
# Folder: server/speck_weg_backend File: training_theme.py
#


from typing import Optional, List, TYPE_CHECKING

from flask.views import MethodView
from sqlalchemy import select, update, bindparam

from ..models import TrainingThemeModel
from .. import db

if TYPE_CHECKING:
    from ..database import CRUD


class TrainingTheme(MethodView):
    def __init__(self,
                 tth_id: int = None, max_sequence: int = None, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.model: Optional['TrainingThemeModel'] = None

        if tth_id:
            stmt = select(TrainingThemeModel).where(TrainingThemeModel.tth_id == tth_id)
            res = db.read_one(stmt)
            self.model = res
        else:
            self.model = None
        self.max_sequence = max_sequence  # current maximum of existing training themes

    def get(self, tth_id: int):
        pass


    def add_theme(self, name: str, description: str):
        self.model = TrainingThemeModel(sequence=self.max_sequence+1)
        self.update_model(name, description)
        self.db.create(self.model)
        # Model saved -> clear for adding another one
        self.model = None
        self.max_sequence += 1  # if other themes are created

    def edit_theme(self, name: str, description: str):
        # updates all attributes (not the sequence, this is done from the collection)
        self.update_model(name, description)
        self.db.update()

    def update_model(self, name: str, description: str):
        self.model.name = name
        self.model.description = description
