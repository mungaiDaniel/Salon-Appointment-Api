from app import db, ma
from datetime import datetime
from flask import jsonify
from enum import Enum
from flask import g 
import logging
import json
from app.utils.auth import jwt, auth
from sqlalchemy.exc import IntegrityError
from passlib.handlers.md5_crypt import md5_crypt
from flask_jwt_extended import get_jwt_identity, create_access_token

class Admin(str, Enum):
    super_admin = 'super_admin'
    admin = 'admin'
    user = 'user'
    


class Users(db.Model):
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    firstName = db.Column(db.String(100))
    lastName = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(1000))
    phoneNumber = db.Column(db.Integer)
    location = db.Column(db.String(100))
    user_role = db.Column(db.Enum(Admin , name='user_roles'), default='user')
    created = db.Column(db.DateTime, default=datetime.utcnow)
    
    
    def __init__(self, firstName, lastName, email, password, phoneNumber, location, user_role='user'):
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.password = password
        self.phoneNumber = phoneNumber
        self.location = location
        self.user_role = user_role

    def as_dict(self):
        return {'id': self.id, 'firstName': self.firstName, 'email': self.email,
                'created': self.created.__format__('%Y-%m-%d'), 'user_role': self.user_role}
    
    def generate_auth_token(self, permission_level):
        
        if permission_level == 2:
            
            token = jwt.dumps({'email': self.email, 'admin': 2})
            
            return token
        elif permission_level == 1:
            
            token = jwt.dumps({'email': self.email, 'admin': 1})
            
            return token
        
        return jwt.dumps({'email': self.email, 'admin': 0})
    
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        
        g.user = None
        
        try:
            
            data = jwt.loads(token)
            
        except Exception as e:
            
            logging.warning('Not verified. {}'.format(e))
            
            return False
        
        if 'email' in data and 'admin' in data:
            
            g.user = data['email']
            
            g.admin = data['admin']
            
            return True
        
        return False
    
    @staticmethod
    def create(firstName, lastName , email, password ,phoneNumber, location ,user_role='user'):

        try:
            user = Users(firstName=firstName, lastName=lastName, email=email ,password=password, phoneNumber=phoneNumber, location=location ,user_role=user_role)

            db.session.add(user)

            db.session.commit()

            return user_schema.jsonify(user)

        except IntegrityError as why:
            
            logging.warning(why)

            return None

        except Exception as why:

            logging.warning(why)

            return None

    
    @staticmethod
    def generate_password_hash(password):

        h = md5_crypt.encrypt(password)

        return h
    
    def verify_password_hash(self, password):

        return md5_crypt.verify(password, self.password)
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'password', 'phoneNumber', 'location', 'user_role', 'created')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True) 


