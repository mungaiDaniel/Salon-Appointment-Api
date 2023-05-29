from app import db, ma
from datetime import datetime
from base_model import Base

class Bookings(Base, db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.DateTime(timezone=True),  nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
        
class Bookingschema(ma.Schema):
    class Meta:
        fields = ('id', 'date', 'time' ,'employee_id' ,'user_id', 'service_id')
        
booking_schema = Bookingschema()
bookings_schemas = Bookingschema(many=True)