# speck_weg
# Stefan Hochuli, 27.09.2021,
# Folder: server/speck_weg_backend File: routes.py
#

from flask import current_app as app, jsonify
from sqlalchemy import select

from .models import WorkoutSessionModel
from .schemas import WorkoutSessionSchema


@app.route('/', methods=['GET'])
def home():
    return jsonify(f'{app.config}')


# sanity check route
@app.route('/ping', methods=['GET'])
def ping_pong():
    return jsonify('pong!')


@app.route('/workout_sessions', methods=['GET'])
def workout_sessions():

    schema = WorkoutSessionSchema()

    stmt = select(WorkoutSessionModel)

    res = app.db_session.execute(stmt).scalars().all()
    print(res)
    # app.session.close() only closes the session, does not end it
    # app.session.remove()
    res = schema.dump(res, many=True)
    print(res)

    return jsonify(res)
