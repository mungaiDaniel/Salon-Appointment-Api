
from base_model import Base
from app.database.database import db



class UserServices(Base, db.Model):
    
    __tablename__ = 'userservices'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'))
    

