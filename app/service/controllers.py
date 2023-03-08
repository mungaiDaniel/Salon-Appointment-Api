from app.service.model import Services, services_schemas, service_schema
from app import db
from app.auth.model import User
from app.utils.responses import m_return
import app.utils.responses as resp
from flask_jwt_extended import  get_jwt_identity


class ServiceController:
    model = Services
    
    @classmethod
    def create_service(cls, data, session):
        
        email = get_jwt_identity()
        user_id= User.query.filter_by(email=email).first()
        service = cls.model(
            style = data.get('style'),
            description = data.get('description'),
            cost = data.get('cost'),
            duration = data.get('duration'),
            user_id = user_id.id,
            created_by = user_id.id
        )
        
        cls.model.save(service, session=session)
        
        return service_schema.jsonify(service)
    
    @classmethod
    def get_all_services(cls, session):
        service = Services.get_all(cls.model, session)
        
        return services_schemas.jsonify(service)
    
    @classmethod
    def get_service_by_id(cls, id, session):
        service = Services.get_one(cls.model, id, session)
        
        return service
        
       
    
    @staticmethod
    def update(id, style, description, cost, duration):
        
        current_style = Services.query.filter_by(id=id).first()
        
        if not current_style:
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
        
    