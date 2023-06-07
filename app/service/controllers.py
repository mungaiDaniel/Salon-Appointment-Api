from app.service.model import Services
from app.schemas.schemas import services_schemas, service_schema
from app.auth.model import User
from app.database.database import db
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
        
        return service_schema.dump(service), 201
    
    @classmethod
    def get_all_services(cls, session):
        service = Services.get_all(cls.model, session)
        
        return services_schemas.dump(service), 200
    
    @classmethod
    def get_service_by_id(cls, id, session):
        service = Services.get_one(cls.model, id, session)

        if service is None:
            return
        
        return service 
        
       
    
    @classmethod
    def update(cls, id, session, style, description, cost, duration):
        
        current_style = Services.get_one(cls.model, id, session)
        
        if not current_style:
            return 
        
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
        
    