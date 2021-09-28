# speck_weg
# Stefan Hochuli, 27.09.2021,
# Folder: server/speck_weg_backend File: routes.py
#

from flask import current_app as app, jsonify
from sqlalchemy import select

from . import db
from .models import WorkoutSessionModel
from .schemas import WorkoutSessionSchema


@app.route('/', methods=['GET'])
def home():
    return jsonify(f'Mis dihei isch dis dihei.')


@app.route('/workout_sessions', methods=['GET'])
def workout_sessions():

    schema = WorkoutSessionSchema()

    stmt = select(WorkoutSessionModel)

    res = db.session.execute(stmt).scalars().all()
    print(res)

    # todo: on dumping, it loads all the relations
    res = schema.dump(res, many=True)
    print(res)

    return jsonify(res)
