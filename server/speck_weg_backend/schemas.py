# speck_weg
# Stefan Hochuli, 28.09.2021,
# Folder: server/speck_weg_backend File: schemas.py
#

# from marshmallow import Schema, fields
# from marshmallow.validate import Length
from marshmallow import pre_load

from .extensions import ma, hash_ctx
from .models import UserModel


class UserSchema(ma.SQLAlchemySchema):
    class Meta:
        model = UserModel

    usr_id = ma.auto_field()
    rid = ma.auto_field()
    first_name = ma.auto_field()  # The length validation is imported from the model
    last_name = ma.auto_field()
    email = ma.auto_field()
    password = ma.auto_field(load_only=True)  # load only?
    weight = ma.auto_field()

    # ORM -> on user not required
    # training_themes = ma.auto_field()

    @pre_load
    def password(self, in_data, **kwargs):
        # Hashes the password on loading
        in_data['password'] = hash_ctx.hash(in_data['password'])


"""
class TrainingThemeSchema(Schema):

    tth_id = fields.Integer()
    name = fields.String(validate=Length(255))
    description = fields.String(validate=Length(1023))
    sequence = fields.Integer()

    training_programs = fields.Nested('TrainingProgramSchema')


class TrainingProgramSchema(Schema):

    tpr_id = fields.Integer()
    tpr_tth_id = fields.Integer(load_only=True)  # no dumping of foreign keys
    name = fields.String(validate=Length(255))
    description = fields.String(validate=Length(1023))
    sequence = fields.Integer()

    training_exercises = fields.Nested('TrainingProgramExerciseSchema', many=True)
    workout_sessions = fields.Nested('WorkoutSessionSchema', many=True)


class TrainingExerciseSchema(Schema):

    tex_id = fields.Integer()
    tex_usr_id = fields.Integer(load_only=True)
    name = fields.String(validate=Length(255))
    description = fields.String(validate=Length(1023))
    baseline_sets = fields.Integer()
    baseline_repetitions = fields.Integer()
    baseline_custom_weight = fields.Float()
    baseline_duration = fields.Float()
    baseline_weight = fields.Float()

    user = fields.Nested(UserSchema, many=False)


class TrainingProgramExerciseSchema(Schema):

    tpe_id = fields.Integer()
    tpe_tpr_id = fields.Integer(load_only=True)
    tpe_tex_id = fields.Integer(load_only=True)
    sequence = fields.Integer()


class WorkoutSessionSchema(Schema):

    wse_id = fields.Integer()
    wse_tpr_id = fields.Integer(load_only=True)
    date = fields.DateTime(timezone=True)
    comment = fields.String(validate=Length(1023))
    score = fields.Float()

    workout_exercises = fields.Nested('WorkoutExerciseSchema', many=True)


class WorkoutExerciseSchema(Schema):

    wex_id = fields.Integer()
    wex_wse_id = fields.Integer(load_only=True)
    wex_tpe_id = fields.Integer(load_only=True)
    sequence = fields.Integer()  # same sequence as in tpe for each exercise
    score = fields.Float()

    workout_sets = fields.Nested('WorkoutSetSchema', many=True)


class WorkoutSetSchema(Schema):

    wst_id = fields.Integer()
    wst_wex_id = fields.Integer(load_only=True)
    set = fields.Integer()
    repetitions = fields.Integer()
    weight = fields.Float()
    duration = fields.Float()
    comment = fields.String(validate=Length(1023))
    score = fields.Float()
"""
