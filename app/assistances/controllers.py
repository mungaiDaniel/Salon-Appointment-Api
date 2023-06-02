from app.assistances.model import UserServices
from app.schemas.schemas import employee_schema
from app.database.database import db
from sqlalchemy.sql import exists
from app.auth.model import User

class UserServicesControll:
    model = UserServices
    
    @classmethod
    def create_assistanceServices(cls, session, service_id, user_id):
        #validate data
        user_exist = session.query(exists().where(User.id == user_id)).scalar()
        
        if not user_exist:
            return {'message': 'user not found'}
        
        assistanceServices = cls.model(
            service_id=service_id,
            user_id=user_id
        )
        cls.model.save(assistanceServices, session=session)
        
        return employee_schema.dump(assistanceServices)