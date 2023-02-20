from app.user import Users, user_schema, users_schema, MyUsers
from flask import request, jsonify, make_response
from app import app, db
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash, generate_password_hash
from flask_jwt_extended import get_jwt_identity, create_access_token



@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    firstName = data['firstName']
    lastName = data['lastName']
    email = data['email']
    password = generate_password_hash(data['password']) 
    phoneNumber = data['phoneNumber']
    location = data['location']
    
    user = Users(firstName=firstName, lastName=lastName, email=email, password=password, phoneNumber=phoneNumber, location=location)
    
    
    db.session.add(user)
    db.session.commit()
    
    return user_schema.jsonify(user), 201

@app.route('/users/<int:id>', methods=['GET'])
def get_one(id):
    my_user = Users.query.get_or_404(id)
    
    return user_schema.dump(my_user), 200

@app.route('/users', methods=['GET'])
def get_all():
    
    my_users = Users.query.all()
    
    results = users_schema.dump(my_users)
    
    return make_response(jsonify({
        "status": 200,
        "data": results
    }), 200)
    
@app.route('/login', methods=['POST'])
def login():
    auth = request.form
    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="Login required !!"'}
        )
    current_user = Users.query.filter_by(email = auth.get('email')).first()
    
    if not current_user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate' : 'Basic realm ="User does not exist !!"'}
        )
   
    if check_password_hash(current_user.password, auth.get('password')):
        token = MyUsers.create_token()
        
        return make_response(jsonify({
            'token': token
        }), 201)
    return make_response(
        'could not verify',
        403,
        {'WWW-Authenticate' : 'Basic realm ="Wrong password !!"'}
    )
    
    