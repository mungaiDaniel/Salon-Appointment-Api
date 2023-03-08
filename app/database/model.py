from app import db, ma, app
from datetime import datetime
from enum import Enum
from base_model import Base
from passlib.handlers.md5_crypt import md5_crypt
from flask_jwt_extended import create_access_token

from base_model import BaseModel

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


        
        
        


