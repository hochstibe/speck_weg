# fingertraining
# Stefan Hochuli, 09.09.2021,
# Folder: speck_weg/app File: workout_exercise.py
#

from typing import Optional, Union, List, TYPE_CHECKING

from sqlalchemy import select, and_
from sqlalchemy.orm import joinedload

from .. import db
from ..models import (
    WorkoutSessionModel, WorkoutExerciseModel,
    TrainingExerciseModel, TrainingProgramExerciseModel
)

if TYPE_CHECKING:
    from ..db import CRUD


class WorkoutExerciseSet:
    def __init__(self, wse: Union[int, 'WorkoutSessionModel'], tpe_id: int):

        # WorkoutSession
        if isinstance(wse, WorkoutSessionModel):
            self.wse_model = wse
        else:
            stmt = select(WorkoutSessionModel).where(WorkoutSessionModel.wse_id == wse)
            self.wse_model: 'WorkoutSessionModel' = db.read_one(stmt)
        # TrainingExercise
        stmt = select(TrainingExerciseModel).join(TrainingProgramExerciseModel).where(
            TrainingProgramExerciseModel.tpe_id == tpe_id).options(
            joinedload(TrainingExerciseModel.user)
        )
        self.tex_model: 'TrainingExerciseModel' = db.read_one(stmt)
        # TrainingProgramExercise
        stmt = select(TrainingProgramExerciseModel).where(
            TrainingProgramExerciseModel.tpe_id == tpe_id)
        self.tpe_model: 'TrainingProgramExerciseModel' = db.read_one(stmt)

        self.wex_model_list: List[Optional['WorkoutExerciseModel']] = [
            None for _ in range(self.tex_model.baseline_sets)
        ]
        # Select the models and replace None (if they exist -> for editing)
        stmt = select(WorkoutExerciseModel).join(TrainingProgramExerciseModel).where(and_(
            WorkoutExerciseModel.wex_wse_id == self.wse_model.wse_id,
            TrainingProgramExerciseModel.tpe_id == tpe_id,
            # WorkoutExerciseModel.sequence == sequence
        )).order_by(WorkoutExerciseModel.set)
        wex_models = list(db.read_stmt(stmt))
        for wex in wex_models:
            self.wex_model_list[wex.set - 1] = wex

    def add_exercise(self, sequence: int, n_set: int, repetitions: int,
                     weight: float, duration: float, comment: str):
        model = WorkoutExerciseModel()
        model.training_exercise = self.tpe_model
        model.workout_session = self.wse_model
        model.sequence = sequence
        model.set = n_set + 1
        self.wex_model_list[n_set] = model

        self.update_model(n_set, repetitions, weight, duration, comment)
        db.update()  # should insert the new model

    def edit_exercise(self, n_set: int, repetitions: int,
                      weight: float, duration: float, comment: str):
        self.update_model(n_set, repetitions, weight, duration, comment)
        db.update()

    def remove_exercise(self, n_set):
        model = self.wex_model_list[n_set]
        db.delete(model)
        self.wex_model_list[n_set] = None

    def update_model(self, n_set: int, repetitions: int,
                     weight: float, duration: float, comment: str):

        model = self.wex_model_list[n_set]

        # Sequence and set is not updated
        model.repetitions = repetitions
        if self.tex_model.baseline_weight:
            model.weight = weight
        if self.tex_model.baseline_duration:
            model.duration = duration
        model.comment = comment
