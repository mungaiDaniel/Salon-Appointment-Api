from app.database.model import Users, user_schema, users_schema
from flask import request
from app import app
import logging
from app.api.auth.model import UserModel
from app.contact.services import Query
import app.utils.responses as resp
from app.utils.responses import m_return 
from app.utils.decorators import permission
from flask_jwt_extended import create_access_token, create_refresh_token ,jwt_required, get_jwt_identity,decode_token


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
    
    user = UserModel.create(firstName=firstName, lastName=lastName, email=email, password=password, phoneNumber=phoneNumber, location=location, user_role='user')
    
    
    if user is None:
        return m_return(http_code=resp.ALREADY_EXIST['http_code'], message=resp.ALREADY_EXIST['message'],
                        code=resp.ALREADY_EXIST['code'])
    
    return user_schema.jsonify(user), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_one(id):
    
    result = Query.get_one(id, Users)
    
    return user_schema.jsonify(result)
        
    

@app.route('/users', methods=['GET'])
def get_all():
    
    results = Query.get_all(Users)
    
    return users_schema.jsonify(results)
   
    
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
        
    refresh_token = create_refresh_token(identity={'email': email})
    
    return m_return(http_code=resp.SUCCESS['http_code'],
                    message=resp.SUCCESS['message'],
                    value={'access_token': access_token, 'refresh_token': refresh_token})
    
@app.route('/admin/<int:id>', methods=['PUT'])
def superAdmin(id):
    
    
    data = request.get_json()
    
    user_role = data['user_role']
    
    admin = UserModel.promote_user(id, user_role=user_role)
    
    return admin

@app.route('/employees', methods=['GET'])
def Admin():
    
    
    results = UserModel.get_admin()
    
    return results