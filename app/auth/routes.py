from app.auth.model import Users, user_schema, users_schema
from flask import request, jsonify, make_response
from app import app, db
import logging
import app.utils.responses as resp
from app.utils.auth import auth, refresh_jwt
from app.utils.responses import m_return 
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from passlib.handlers.md5_crypt import md5_crypt
from app.utils.decorators import permission
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import get_jwt_identity, create_access_token


@app.after_request
def add_header(response):
    response.headers['Access-Control-Allow-Origin'] = '*'
    return response

@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    try:    
        firstName = data['firstName']
        lastName = data['lastName']
        email = data['email']
        password = Users.generate_password_hash(data['password']) 
        phoneNumber = data['phoneNumber']
        location = data['location']
        
    except Exception as why:
        
        logging.warning(why)
        
        return m_return(http_code=resp.MISSED_PARAMETERS['http_code'], message=resp.MISSED_PARAMETERS['message'],
                        code=resp.MISSED_PARAMETERS['code'])
    
    
    
    user = Users(firstName=firstName, lastName=lastName, email=email, password=password, phoneNumber=phoneNumber, location=location, user_role='user')
    
    db.session.add(user)

    db.session.commit()
    
    if user is None:

        # Return already exists error.
        return m_return(http_code=resp.ALREADY_EXIST['http_code'], message=resp.ALREADY_EXIST['message'],
                        code=resp.ALREADY_EXIST['code'])
    
    return user_schema.jsonify(user), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_one(id):
    my_user = Users.query.get_or_404(id)
    
    return user_schema.dump(my_user), 200

@app.route('/users', methods=['GET'])
def get_all():
    
    my_users = Users.query.all()
    
    results = users_schema.dump(my_users)
    
    return  {'data': results}, 200
   
    
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
        
    user = Users.query.filter_by(email=email).first()
    
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
        
    ref_token = refresh_jwt.dumps({'email': email})
    
    return m_return(http_code=resp.SUCCESS['http_code'],
                    message=resp.SUCCESS['message'],
                    value={'access_token': access_token, 'refresh_token': ref_token})