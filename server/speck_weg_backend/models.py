# speck_weg
# Stefan Hochuli, 24.09.2021,
# Folder: server/speck_weg_backend File: models.py
#

from typing import Tuple, TYPE_CHECKING

from sqlalchemy import FetchedValue
from sqlalchemy.sql import func

from .extensions import db
from .database.functions import random_number_func, random_id_func, \
    update_baseline_weight_func, update_set_score_func,     \
    update_exercise_score_func, update_session_score_func,    \
    user_weight_updated_func, baseline_weight_updated_func,      \
    set_score_updated_func, exercise_score_updated_func
from .database.triggers import update_baseline_weight_trigger, update_set_score_trigger, \
    update_exercise_score_trigger, update_session_score_trigger, \
    user_weight_updated_trigger, baseline_weight_updated_trigger, \
    set_score_updated_trigger, exercise_score_updated_trigger, \
    random_id_user_trigger, random_id_training_theme_trigger, \
    random_id_training_program_trigger, random_id_training_program_exercise_trigger, \
    random_id_training_exercise_trigger, random_id_workout_session_trigger, \
    random_id_workout_exercise_trigger, random_id_workout_set_trigger


if TYPE_CHECKING:
    from sqlalchemy import DDL


class HeroModel(db.Model):
    __tablename__ = 'hero'

    id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    name = db.Column(db.String, nullable=False)


class UserModel(db.Model):
    # table definitions
    __tablename__ = 'user'

    usr_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    weight = db.Column(db.Float, nullable=False)

    training_themes = db.relationship('TrainingThemeModel', back_populates='user')
    training_exercises = db.relationship('TrainingExerciseModel', back_populates='user')

    def __repr__(self):
        return f'UserModel(usr_id={self.usr_id}, name={self.name} weight={self.weight}'


class TrainingThemeModel(db.Model):
    # table definitions
    __tablename__ = 'training_theme'
    __table_args__ = (
        db.UniqueConstraint('name'),
    )

    tth_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    tth_usr_id = db.Column(db.ForeignKey('user.usr_id'), nullable=False)
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(1023), nullable=True)
    sequence = db.Column(db.Integer, nullable=False)

    # orm definitions
    user = db.relationship('UserModel', back_populates='training_themes')
    training_programs = db.relationship(
        'TrainingProgramModel', back_populates='training_theme',
        order_by='asc(TrainingProgramModel.sequence), asc(TrainingProgramModel.name)')

    def __repr__(self):
        return f'TrainingThemeModel(' \
               f'tth_id={self.tth_id!r}, name={self.name!r})'


class TrainingProgramModel(db.Model):
    # table definitions
    __tablename__ = 'training_program'
    __table_args__ = (
        db.UniqueConstraint('tpr_tth_id', 'name'),
    )

    tpr_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    tpr_tth_id = db.Column(db.ForeignKey('training_theme.tth_id'), nullable=False)
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(1023), nullable=True)
    sequence = db.Column(db.Integer, nullable=False)

    # orm definitions
    training_theme = db.relationship('TrainingThemeModel', back_populates='training_programs')
    training_exercises = db.relationship(
        'TrainingProgramExerciseModel', back_populates='training_program',
        order_by='asc(TrainingProgramExerciseModel.sequence)')
    workout_sessions = db.relationship('WorkoutSessionModel', back_populates='training_program')

    def __repr__(self):
        return f'TrainingProgramModel(' \
               f'tpr_id={self.tpr_id!r}, name={self.name!r})'


class TrainingExerciseModel(db.Model):
    # table definitions
    __tablename__ = 'training_exercise'
    # No unique constraint: Multiple exercises with the same name possible (2x half crimp big)

    tex_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    tex_usr_id = db.Column(db.Integer, db.ForeignKey('user.usr_id'), nullable=True)
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    name = db.Column(db.String(63), nullable=False)
    description = db.Column(db.String(1023), nullable=True)
    baseline_sets = db.Column(db.Integer, nullable=False)
    baseline_repetitions = db.Column(db.Integer, nullable=False)
    baseline_custom_weight = db.Column(db.Float, nullable=True)
    baseline_duration = db.Column(db.Float, nullable=True)
    baseline_weight = db.Column(db.Float, nullable=True)

    # orm definitions
    training_programs = db.relationship(  # todo cascade? -> only, if no other tpe is around
        'TrainingProgramExerciseModel', back_populates='training_exercise', cascade="all, delete")
    user = db.relationship('UserModel', back_populates='training_exercises')

    def __repr__(self):
        return f'TrainingExerciseModel(' \
               f'tex_id={self.tex_id!r}, name={self.name!r})'


class TrainingProgramExerciseModel(db.Model):
    # table definitions
    __tablename__ = 'training_program_exercise'

    tpe_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    tpe_tpr_id = db.Column(db.ForeignKey('training_program.tpr_id'), nullable=False)
    tpe_tex_id = db.Column(db.ForeignKey('training_exercise.tex_id'), nullable=False)
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    sequence = db.Column(db.Integer, nullable=False)

    # orm definitions
    training_program = db.relationship(
        'TrainingProgramModel', back_populates='training_exercises')
    training_exercise = db.relationship(
        'TrainingExerciseModel', back_populates='training_programs')
    workout_exercises = db.relationship(
        'WorkoutExerciseModel', back_populates='training_exercise')

    def __repr__(self):
        return f'TrainingProgramExerciseModel(tpe_id={self.tpe_id}, ' \
               f'tpe_tpr_id=({self.tpe_tpr_id!r}, tpe_tex_id={self.tpe_tex_id}, ' \
               f'sequence={self.sequence})'


class WorkoutSessionModel(db.Model):
    # table definitions
    __tablename__ = 'workout_session'

    wse_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    wse_tpr_id = db.Column(db.ForeignKey('training_program.tpr_id'))
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    date = db.Column(db.DateTime(timezone=True), nullable=False,
                     server_default=func.current_timestamp())
    comment = db.Column(db.String(1023), nullable=True)
    score = db.Column(db.Float, nullable=False,
                      server_default=FetchedValue(), server_onupdate=FetchedValue())

    # orm definitions
    training_program = db.relationship('TrainingProgramModel', back_populates='workout_sessions')
    workout_exercises = db.relationship(
        'WorkoutExerciseModel', back_populates='workout_session',
        order_by='asc(WorkoutExerciseModel.sequence)')

    def __repr__(self):
        return f'WorkoutSessionModel(' \
               f'wse_id=({self.wse_id!r}, tse_tpr_id={self.wse_tpr_id}, date={self.date},' \
               f' score={self.score})'


class WorkoutExerciseModel(db.Model):
    # table definitions
    __tablename__ = 'workout_exercise'

    wex_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    wex_wse_id = db.Column(db.ForeignKey('workout_session.wse_id'))
    wex_tpe_id = db.Column(db.ForeignKey('training_program_exercise.tpe_id'))
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    sequence = db.Column(db.Integer, nullable=False)  # same sequence as in tpe for each exercise
    score = db.Column(db.Float, nullable=True,  # Todo: other scores work with nullable=False
                      server_default=FetchedValue(), server_onupdate=FetchedValue())

    # orm definitions
    workout_session = db.relationship('WorkoutSessionModel', back_populates='workout_exercises')
    training_exercise = db.relationship(
        'TrainingProgramExerciseModel', back_populates='workout_exercises')
    workout_sets = db.relationship(
        'WorkoutSetModel', back_populates='workout_exercise',
        order_by='asc(WorkoutSetModel.set)')

    def __repr__(self):
        return f'WorkoutExerciseModel(' \
               f'wex_id={self.wex_id}, wex_wse_id={self.wex_wse_id},' \
               f' wex_tpe_id={self.wex_tpe_id}, sequence={self.sequence}, score={self.score})'


class WorkoutSetModel(db.Model):
    # table definitions
    __tablename__ = 'workout_set'

    wst_id = db.Column(db.Integer, primary_key=True, autoincrement='auto')
    wst_wex_id = db.Column(db.ForeignKey('workout_exercise.wex_id'))
    rid = db.Column(db.Integer, nullable=False, index=True,
                    server_default=FetchedValue(), server_onupdate=FetchedValue())
    set = db.Column(db.Integer, nullable=False)
    repetitions = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=True)
    duration = db.Column(db.Float, nullable=True)
    comment = db.Column(db.String(1023), nullable=True)
    score = db.Column(db.Float, nullable=False,
                      server_default=FetchedValue(), server_onupdate=FetchedValue())

    # orm definitions
    workout_exercise = db.relationship('WorkoutExerciseModel', back_populates='workout_sets')

    def __repr__(self):
        return f'WorkoutSetModel(' \
               f'wst_id={self.wst_id}, wst_wex_id={self.wst_wex_id}, set={self.set},' \
               f' score={self.score})'


def register_ddl(mod, ddl_list: Tuple['DDL']):
    # Add the functions to the database (register to the specific tables)
    for trigger in ddl_list:
        db.event.listen(
            mod.__table__,
            'after_create',
            trigger.execute_if(dialect='postgresql')
        )


function_list = [
    # random number / id are needed only once for all triggers
    (UserModel, (user_weight_updated_func, random_number_func, random_id_func)),
    (TrainingThemeModel, ()),
    (TrainingProgramModel, ()),
    (TrainingProgramExerciseModel, ()),
    (TrainingExerciseModel, (update_baseline_weight_func, baseline_weight_updated_func)),
    (WorkoutSetModel, (update_set_score_func, set_score_updated_func)),
    (WorkoutExerciseModel, (update_exercise_score_func, exercise_score_updated_func)),
    (WorkoutSessionModel, (update_session_score_func, )),
]

trigger_list = [
    (UserModel, (user_weight_updated_trigger, random_id_user_trigger)),
    (TrainingThemeModel, (random_id_training_theme_trigger, )),
    (TrainingProgramModel, (random_id_training_program_trigger, )),
    (TrainingProgramExerciseModel, (random_id_training_program_exercise_trigger, )),
    (TrainingExerciseModel, (update_baseline_weight_trigger, baseline_weight_updated_trigger,
                             random_id_training_exercise_trigger)),
    (WorkoutSetModel, (update_set_score_trigger, set_score_updated_trigger,
                       random_id_workout_set_trigger)),
    (WorkoutExerciseModel, (update_exercise_score_trigger, exercise_score_updated_trigger,
                            random_id_workout_exercise_trigger)),
    (WorkoutSessionModel, (update_session_score_trigger, random_id_workout_session_trigger)),
]


for model, functions in function_list:
    register_ddl(model, functions)

for model, triggers in trigger_list:
    register_ddl(model, triggers)
