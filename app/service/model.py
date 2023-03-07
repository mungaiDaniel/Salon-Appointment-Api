from app.database.model import Services, service_schema, services_schemas
from app import db
from app.utils.responses import m_return
import app.utils.responses as resp
from base_model import Base


class Services(Base,db.Model):
    __tablename__ = 'services'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(100))
    description = db.Column(db.String(500))
    cost = db.Column(db.Float)
    duration = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

class ServiceModel:
    
    @staticmethod
    def create_service(style, description, cost, duration, user_id):
        
        service = Services(style=style, description=description, cost=cost, duration=duration, user_id=user_id) 

        db.session.add(service)
        db.session.commit()
        
        return service
    
    @staticmethod
    def get_all(table):
        service = db.session.query(table).all()
        
        
        return service
    
    @classmethod
    def get_one(cls, id):
        
        service = Services.query.filter_by(id=id).first()
        
        if not service:
            return m_return(http_code=resp.NOT_FOUND_404['http_code'],
                        message=resp.NOT_FOUND_404['message'],
                        code=resp.NOT_FOUND_404['code'])
        
        result = service_schema.jsonify(service)
        
        return result
    
    @staticmethod
    def update(id, style, description, cost, duration):
        
        current_style = Services.query.filter_by(id=id).first()
        
        if current_style is None:
            return {'message': 'no style found by that id'}
        
        current_style.style = style
        current_style.description = description
        current_style.cost = cost
        current_style.duration = duration
        

        db.session.commit()
        
        return current_style
    
    @classmethod
    def delete(cls, service):
        
        
        db.session.delete(service)
        db.session.commit()
        
        return m_return(http_code=resp.DELETED_SUCCESS['http_code'],
                        message=resp.DELETED_SUCCESS['message'],
                        code=resp.DELETED_SUCCESS['code'])
        
    