# speck_weg
# Stefan Hochuli, 14.10.2021,
# Folder: server/speck_weg_backend/routes File: heroes.py
#

from flask import jsonify, request, make_response
from flask.views import MethodView
from sqlalchemy import select, update, delete, func
from marshmallow import EXCLUDE

from ..models import HeroModel
from ..schemas import HeroSchema
from ..extensions import db


class HeroAPI(MethodView):
    # One API for access to single and collection

    schema = HeroSchema()

    def get_single(self, hero_id):

        stmt = select(HeroModel).where(HeroModel.id == hero_id)
        res = db.read_one(stmt)

        print(res)
        res = self.schema.dump(res, many=False)

        return res

    def get_collection(self):

        name = request.args.get('name', None)

        if name:
            stmt = select(HeroModel).where(  # case insensitive search
                HeroModel.name.ilike(f'%{name}%')).order_by(HeroModel.name)

        else:
            stmt = select(HeroModel).order_by(HeroModel.name)

        res = db.read_stmt(stmt)

        res = self.schema.dump(res, many=True)

        return res

    def get(self, hero_id):
        if hero_id:
            res = self.get_single(hero_id)

        else:
            res = self.get_collection()

        return jsonify(res)

    def post(self):

        data = request.json
        data = self.schema.load(data, unknown=EXCLUDE, many=False)

        model = HeroModel(**data)
        db.create(model)
        res = self.schema.dump(model, many=False)

        return jsonify(res)

    def put(self, hero_id):

        data = request.json
        print(data)

        # Try to update the user
        data = self.schema.load(data, unknown=EXCLUDE)
        print(data)

        stmt = update(HeroModel).where(HeroModel.id == hero_id)
        db.update(stmt=stmt, payload=data)
        # Todo: return codes, return the persisted object?

        return make_response(jsonify(), 204)

    @staticmethod
    def delete(hero_id):

        stmt = delete(HeroModel).where(HeroModel.id == hero_id)
        db.delete_stmt(stmt)

        return make_response(jsonify(), 204)
