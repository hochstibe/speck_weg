# speck_weg
# Stefan Hochuli, 27.09.2021,
# Folder: server/speck_weg_backend File: routes.py
#

from flask import current_app as app, jsonify, request, make_response
from sqlalchemy import select, update, delete
from marshmallow import EXCLUDE

from .extensions import db
from .models import WorkoutSessionModel, HeroModel
from .schemas import HeroSchema
# from .schemas import WorkoutSessionSchema

"""
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



@app.route('/heroes', methods=['GET'])
def get_heroes():
    schema = HeroSchema()
    stmt = select(HeroModel).order_by(HeroModel.name)
    res = db.read_stmt(stmt)
    print(res)

    res = schema.dump(res, many=True)

    return jsonify(res)


@app.route('/heroes', methods=['POST'])
def new_hero():
    schema = HeroSchema()
    data = request.json
    data = schema.load(data, unknown=EXCLUDE, many=False)

    model = HeroModel(**data)
    db.create(model)
    res = schema.dump(model, many=False)

    return jsonify(res)


@app.route('/heroes/<int:hid>', methods=['GET'])
def get_hero(hid):
    schema = HeroSchema()
    stmt = select(HeroModel).where(HeroModel.id == hid)
    res = db.read_one(stmt)

    print(res)
    res = schema.dump(res, many=False)

    return jsonify(res)


@app.route('/heroes/<int:hid>', methods=['PUT'])
def update_hero(hid):
    schema = HeroSchema()

    data = request.json
    print(data)

    # Try to update the user

    data = schema.load(data, unknown=EXCLUDE)
    print(data)

    stmt = update(HeroModel).where(HeroModel.id == hid)
    db.update(stmt=stmt, payload=data)
    # Todo: return codes
    return make_response('', 204)


@app.route('/heroes/<int:hid>', methods=['DELETE'])
def delete_hero(hid):

    stmt = delete(HeroModel).where(HeroModel.id == hid)
    db.update(stmt)

    return make_response('', 201)
"""
