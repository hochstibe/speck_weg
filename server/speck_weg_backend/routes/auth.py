# speck_weg
# Stefan Hochuli, 15.10.2021,
# Folder: server/speck_weg_backend/routes File: auth.py
#

from http import HTTPStatus

from flask import request, jsonify, make_response
from flask_jwt_extended import create_access_token, set_access_cookies, unset_jwt_cookies
from sqlalchemy import select

from . import auth_bp
from ..extensions import db, hash_ctx
from ..schemas import UserSchema
from ..models import UserModel

# Todo: Automatic user-loading (current user)
# Todo: refresh the tokens


@auth_bp.route('/register', methods=['POST'])
def register():

    schema = UserSchema(many=False)

    data = request.json
    data = schema.load(data)

    usr = UserModel(**data)
    db.create(usr)

    print(HTTPStatus.NO_CONTENT, HTTPStatus.NO_CONTENT.value)

    return make_response(jsonify(), HTTPStatus.NO_CONTENT.value)


@auth_bp.route('/login', methods=['POST'])
def login():

    email = request.json.get("email", None)
    password = request.json.get("password", None)

    print(HTTPStatus.UNAUTHORIZED, HTTPStatus.UNAUTHORIZED.value)

    unauthorized_msg = make_response(jsonify({"msg": "Bad username or password"}),
                               HTTPStatus.UNAUTHORIZED.value)

    # email and password required
    if not email or not password:
        return unauthorized_msg

    # Get the user by the email
    stmt = select(UserModel).where(UserModel.email == email)
    usr = db.read_one(stmt)

    if not usr:
        return unauthorized_msg

    # Verify the password
    if hash_ctx.verify(password, usr.password):
        # password and stored hash match
        access_token = create_access_token(identity=usr.rid)
        response = jsonify(access_token=access_token)
        set_access_cookies(response, access_token)
        return response
    else:
        # Password and hash dont match
        return unauthorized_msg


@auth_bp.route('/logout', methods=['POST'])
def logout_with_cookies():
    response = jsonify({'msg': 'logout successful'})
    unset_jwt_cookies(response)
    return response
