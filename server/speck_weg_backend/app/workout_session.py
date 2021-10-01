# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: workout_session.py
#

from typing import List, Tuple, Optional, Union

from sqlalchemy import select
from sqlalchemy.orm import joinedload

from .. import db
from .workout_exercise import WorkoutExerciseSet
from ..models import (TrainingProgramModel, WorkoutSessionModel)


class WorkoutSession:
    def __init__(self, tpr: Union[int, 'TrainingProgramModel'] = None,
                 wse: Union[int, 'WorkoutSessionModel'] = None, **kwargs):
        """
        Either the  the WorkoutSession is given (TrainingProgram is fetched from the orm)
        or the TrainingProgram is given (no Workout session yet)

        :param tpr:
        :param wse:
        :param kwargs:
        """
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        # read the objects from the database
        self.model = None
        if isinstance(wse, WorkoutSessionModel):
            self.model = wse
            self.tpr_model = self._read_tpr_id(wse.wse_tpr_id)
        elif isinstance(tpr, TrainingProgramModel):
            self.tpr_model = tpr
            self.model = None
        else:
            # Load from the ids
            self.tpr_model, self.model = self.read_objects(tpr, wse)

        if not self.model:
            # Start a new session
            self.add_session()

        # Generate a list for all exercises (planned and done exercise sets)
        self.exercises = [WorkoutExerciseSet(self.model, tpe.tpe_id)
                          for tpe in self.tpr_model.training_exercises]

    @property
    def wex_saved(self):
        wex_models = [wex for wex_set in self.exercises
                      for wex in wex_set.wex_model_list]
        if any(wex_models):
            return True
        else:
            return False

    @staticmethod
    def _read_wse_id(wse_id: int) -> 'WorkoutSessionModel':
        # Load the WorkoutSession and the TrainingProgram
        # Todo: load also the TrainingTheme and the TrainingProgramExercises
        stmt = select(WorkoutSessionModel).where(WorkoutSessionModel.wse_id == wse_id)
        model = db.read_one(stmt)

        return model

    @staticmethod
    def _read_tpr_id(tpr_id: int) -> 'TrainingProgramModel':
        # No WorkoutSession yet, load the TrainingProgram / Theme (name is needed for the gui)
        stmt = select(TrainingProgramModel).where(
            TrainingProgramModel.tpr_id == tpr_id).options(
            joinedload(TrainingProgramModel.training_theme, innerjoin=True),
            joinedload(TrainingProgramModel.training_exercises)
        )
        parent_model = db.read_one(stmt, unique=True)
        return parent_model

    def read_objects(self, tpr_id: int = None, wse_id: int = None
                     ) -> Tuple['TrainingProgramModel', Optional['WorkoutSessionModel']]:

        if wse_id:
            model = self._read_wse_id(wse_id)
            parent_model = self._read_tpr_id(model.wse_tpr_id)
        elif tpr_id:
            # No WorkoutSession yet, load the TrainingProgram
            parent_model = self._read_tpr_id(tpr_id)
            model = None
        else:
            raise ValueError('Either wse_id or tpr_id must be given')
        return parent_model, model

    def add_session(self):
        self.model = WorkoutSessionModel()
        self.model.training_program = self.tpr_model
        db.create(self.model)

    def edit_session(self, comment: str):
        self.model.comment = comment
        db.update()

    def remove_session(self):
        # Deletes the session and all the exercises

        # Create a list of all existing wex models
        # model_list = []
        # for wex_set in self.workout_session.exercises:
        #     for wex in wex_set.wex_model_list:
        #         if wex:
        #             model_list.append(wex)

        model_list = [wex for wex_set in self.exercises
                      for wex in wex_set.wex_model_list if wex]
        # Add the wse to the list
        if self.model:
            model_list.append(self.model)
        db.delete(model_list)

        # remove from the lists
        self.model = None
        for wex_set in self.exercises:
            wex_set.wex_model_list = [None for _ in wex_set.wex_model_list]
        print('models after delete:', self.model, [wex_set.wex_model_list
                                                   for wex_set in self.exercises])


class WorkoutSessionCollection:
    def __init__(self, **kwargs):
        # Additional arguments are passed to next inheritance
        super().__init__(**kwargs)

        self.workout_list: List['WorkoutSession'] = []

    def read_sessions(self, tpr_id: int = None, tth_id: int = None):

        if tpr_id:
            stmt = select(WorkoutSessionModel).where(
                WorkoutSessionModel.wse_tpr_id == tpr_id).order_by(
                WorkoutSessionModel.date)
        elif tth_id:
            stmt = select(WorkoutSessionModel).join(WorkoutSessionModel.training_program).where(
                TrainingProgramModel.tpr_tth_id == tth_id).order_by(
                WorkoutSessionModel.date)
        else:
            stmt = select(WorkoutSessionModel).order_by(
                WorkoutSessionModel.date)

        model_list = list(db.read_stmt(stmt))
        self.workout_list = [WorkoutSession(self.db, wse=wse) for wse in model_list]
