from app import db, ma
import datetime
from flask import jsonify
from passlib.handlers.pbkdf2 import pbkdf2_sha256
from flask_jwt_extended import get_jwt_identity, create_access_token

class Users(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    phoneNumber = db.Column(db.Integer)
    location = db.Column(db.String(100))
    
    
    def __init__(self, firstName, lastName, email, password, phoneNumber, location):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.location = location
class MyUsers:
    @staticmethod
    def generate_hash(password):
        return pbkdf2_sha256.hash(password)
    
    @staticmethod
    def verify_hash(password, hash):
        return pbkdf2_sha256.verify(password, hash)
    
    @staticmethod
    def create_token():
        email = get_jwt_identity()
        expires = datetime.datetime.utcnow() + datetime.timedelta(days=1, seconds=5)
        token = create_access_token(email, expires_delta=expires)
        return jsonify({'token': token})
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'password', 'phoneNumber', 'location')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True) 


