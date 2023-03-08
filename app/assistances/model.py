
from base_model import Base
from app import db , ma



class UserServices(Base, db.Model):
    
    __tablename__ = 'userservices'
    # __table_args__ = {'extend_existing': True}
    # __abstract__ = True
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    

class Employeeschema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'service_id')
        
employee_schema = Employeeschema()
employees_schemas = Employeeschema(many=True)