import json

from app.auth.controllers import UserController
from app.database.model import user_schema, users_schema
from flask import request
from app import app, db
from app.auth.model import User
import logging
from app.utils.services import Query
import app.utils.responses as resp
from app.utils.responses import m_return
from app.utils.decorators import permission
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, decode_token



@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    session = db.session
    return UserController.create_user(data, session=session)


@app.route('/users/<int:id>', methods=['GET'])
def get_one(id):
    result = Query.get_one(id, User)

    return user_schema.jsonify(result)


# @app.route('/users', methods=['GET'])
# def get_all():
#     results = Query.get_all(Users)
#
#     return users_schema.jsonify(results)


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    try:
        email = data['email']
        password = (data['password'])

    except Exception as why:

        logging.info('Email or password is wrong' + str(why))

        return m_return(http_code=resp.MISSED_PARAMETERS['http_code'], message=resp.MISSED_PARAMETERS['message'],
                        code=resp.MISSED_PARAMETERS['code'])

    user = User.query.filter_by(email=email).first()

    if user is None:
        return m_return(http_code=resp.USER_DOES_NOT_EXIST['http_code'],
                        message=resp.USER_DOES_NOT_EXIST['message'],
                        code=resp.USER_DOES_NOT_EXIST['code'])

    if not user.verify_password_hash(password):
        return m_return(http_code=resp.CREDENTIALS_ERROR_999['http_code'],
                        message=resp.CREDENTIALS_ERROR_999['message'], code=resp.CREDENTIALS_ERROR_999['code'])

    if user.user_role == 'user':

        access_token = user.generate_auth_token(0)

    elif user.user_role == 'admin':

        # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
        access_token = user.generate_auth_token(1)

    elif user.user_role == 'super_admin':

        # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
        access_token = user.generate_auth_token(2)

    else:

        # Return permission denied error.
        return m_return(http_code=resp.PERMISSION_DENIED['http_code'], message=resp.PERMISSION_DENIED['message'],
                        code=resp.PERMISSION_DENIED['code'])

    refresh_token = create_refresh_token(identity={'email': email})

    return m_return(http_code=resp.SUCCESS['http_code'],
                    message=resp.SUCCESS['message'],
                    value={'access_token': access_token, 'refresh_token': refresh_token})


# @app.route('/admin/<int:id>', methods=['PUT'])
# def superAdmin(id):
#     data = request.get_json()

#     user_role = data['user_role']

#     admin = UserModel.promote_user(id, user_role=user_role)

#     return admin


# @app.route('/employees', methods=['GET'])
# def Admin():
#     results = UserModel.get_admin()

#     return results
