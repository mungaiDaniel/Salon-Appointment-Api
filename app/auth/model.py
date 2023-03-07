import datetime
from sqlalchemy import Column, Integer, String, DateTime, Enum, UniqueConstraint

from app.database.model import  user_schema, users_schema
from app import db
from app.utils.responses import m_return
import app.utils.responses as resp
from base_model import Base
from flask_jwt_extended import create_access_token
from passlib.handlers.md5_crypt import md5_crypt


class Admin(str, Enum):
    super_admin = 'super_admin'
    admin = 'admin'
    user = 'user'


class User(Base, db.Model):
    __tablename__ = 'user'
   

    id = Column(Integer, primary_key=True)
    firstName = Column(String(100))
    lastName = db.Column(String(100))
    email = Column(String(100), unique=True)
    password = Column(String(1000))
    phoneNumber = Column(Integer)
    location = Column(String(100))
    user_role = Column(String,  Enum('super_admin', 'admin', 'user', name='user_roles'), default='user')
    created = Column(DateTime, default=datetime.datetime.now())
    
    # def __init__(self, firstName, lastName, email, password, phoneNumber, location, user_role='user'):
    #     self.firstName = firstName
    #     self.lastName = lastName
    #     self.email = email
    #     self.password = password
    #     self.phoneNumber = phoneNumber
    #     self.location = location
    #     self.user_role = user_role
        
    def generate_auth_token(self, permission_level):
    
    
        if permission_level == 2:
    
            token = create_access_token(identity=self.email, additional_claims= {'admin': 2})
    
            return token
        elif permission_level == 1:
    
            token = create_access_token(identity= self.email, additional_claims= {'admin': 1})
    
            return token
    
        return create_access_token(identity=self.email, additional_claims= {'admin': 0})
    
    @staticmethod
    def generate_password_hash(password):
    
        h = md5_crypt.hash(password)
    
        return h
    
    def verify_password_hash(self, password):
    
        return md5_crypt.verify(password, self.password)
    

# class UserSchema(ma.Schema):
#     class Meta:
#         fields = (
#         'id', 'firstName', 'lastName', 'email', 'password', 'phoneNumber', 'location', 'user_role', 'created')
#
# user_schema = UserSchema()
# users_schema = UserSchema(many=True)


# class UserModel:
#
#     @staticmethod
#     def create(firstName, lastName, email, password, phoneNumber, location, user_role='user'):
#         user = Users(firstName=firstName, lastName=lastName, email=email, password=password, phoneNumber=phoneNumber,
#                      location=location, user_role=user_role)
#
#         db.session.add(user)
#         db.session.commit()
#
#         return user
#
#     @classmethod
#     def get_one(cls, id):
#
#         user = Users.query.filter_by(id=id).first()
#
#         if not user:
#             return m_return(http_code=resp.USER_DOES_NOT_EXIST['http_code'],
#                             message=resp.USER_DOES_NOT_EXIST['message'],
#                             code=resp.USER_DOES_NOT_EXIST['code'])
#
#         result = user_schema.jsonify(user)
#
#         return result
#
#     @staticmethod
#     def get_admin():
#         user_role = 'admin'
#         employe = Users.query.filter_by(user_role=user_role).all()
#         result = users_schema.jsonify(employe)
#
#         return result
#
#     @classmethod
#     def promote_user(cls, id, user_role):
#
#         admin = Users.query.get_or_404(id)
#
#         admin.user_role = user_role
#
#         if user_role == 'super_admin' or user_role == 'admin':
#             admin.user_role = user_role
#
#         db.session.commit()
#
#         return user_schema.jsonify(admin), 200
