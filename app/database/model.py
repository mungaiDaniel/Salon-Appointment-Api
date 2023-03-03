from app import db, ma, app
from datetime import datetime
from enum import Enum
from passlib.handlers.md5_crypt import md5_crypt
from flask_jwt_extended import create_access_token


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
    created = db.Column(db.DateTime, default=datetime.now())
    
    
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
    
    @staticmethod
    def create(firstName, lastName, email, password, phoneNumber, location, user_role='user'):
        user = Users(firstName=firstName, lastName=lastName, email=email,password=password, phoneNumber=phoneNumber, location=location,user_role=user_role)
        
        db.session.add(user)
        db.session.commit()
        
        return user
        
        
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
        
class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'firstName', 'lastName', 'email', 'password', 'phoneNumber', 'location', 'user_role', 'created')
        
user_schema = UserSchema()
users_schema = UserSchema(many=True) 

class Services(db.Model):
    __tablename__ = 'services'
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(100))
    description = db.Column(db.String(500))
    cost = db.Column(db.Float)
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
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
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
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
    employee_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
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


        
        
        


