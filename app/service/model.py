from app.database.database import db
from base_model import Base


class Services(Base, db.Model):
    __tablename__ = 'services'
    __table_args__ = {'extend_existing': True}
    
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(100))
    description = db.Column(db.String(500))
    cost = db.Column(db.Float)
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

