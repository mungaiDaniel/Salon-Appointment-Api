from app.user import Users, user_schema, users_schema
from flask import request, jsonify, make_response
from app import app, db
import json



@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    
    FirstName = data['FirstName']
    LastName = data['LastName']
    Email = data['Email']
    Password = data['Password']
    PhoneNumber = data['PhoneNumber']
    Location = data['Location']
    
    user = Users(FirstName=FirstName, LastName=LastName, Email=Email, Password=Password, PhoneNumber=PhoneNumber, Location=Location)
    
    
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