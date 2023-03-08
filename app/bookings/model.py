from app import db, ma
from datetime import datetime
from base_model import Base

class Bookings(Base, db.Model):
    __tablename__ = 'bookings'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.DateTime,
        default=datetime.utcnow())
    employee_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
        
class Bookingschema(ma.Schema):
    class Meta:
        fields = ('id', 'time', 'employee_id' ,'user_id', 'service_id')
        
booking_schema = Bookingschema()
bookings_schemas = Bookingschema(many=True)