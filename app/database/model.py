from app import db, ma, app
from datetime import datetime
from enum import Enum
from base_model import Base
from passlib.handlers.md5_crypt import md5_crypt
from flask_jwt_extended import create_access_token

from base_model import BaseModel



        
    # def generate_auth_token(self, permission_level):
    #
    #
    #     if permission_level == 2:
    #
    #         token = create_access_token(identity=self.email, additional_claims= {'admin': 2})
    #
    #         return token
    #     elif permission_level == 1:
    #
    #         token = create_access_token(identity= self.email, additional_claims= {'admin': 1})
    #
    #         return token
    #
    #     return create_access_token(identity=self.email, additional_claims= {'admin': 0})
    #
    # @staticmethod
    # def generate_password_hash(password):
    #
    #     h = md5_crypt.hash(password)
    #
    #     return h
    #
    # def verify_password_hash(self, password):
    #
    #     return md5_crypt.verify(password, self.password)
        


class Services(Base, db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(100))
    description = db.Column(db.String(500))
    cost = db.Column(db.Float)
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, style, description, cost, duration, user_id):
        self.style = style
        self.description = description
        self.cost = cost
        self.duration = duration
        self.user_id = user_id
        
class Serviceschema(ma.Schema):
    class Meta:
        fields = ('id', 'style', 'description', 'cost', 'duration', 'user_id')
        
service_schema = Serviceschema()
services_schemas = Serviceschema(many=True)

class UserServices(db.Model):
    
    __tablename__ = 'userservices'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    
    def __init__(self, user_id, service_id):
        self.user_id = user_id
        self.service_id = service_id

class Employeeschema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'service_id')
        
employee_schema = Employeeschema()
employees_schemas = Employeeschema(many=True)

class Bookings(db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime,
        default=datetime.utcnow())
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __init__(self, time, employee_id, service_id, user_id):
        self.time = time
        self.employee_id = employee_id
        self.service_id = service_id
        self.user_id = user_id
        
class Bookingschema(ma.Schema):
    class Meta:
        fields = ('id', 'time', 'employee_id' ,'user_id', 'service_id')
        
booking_schema = Bookingschema()
bookings_schemas = Bookingschema(many=True)


        
        
        


