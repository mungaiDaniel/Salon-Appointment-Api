from app.database.model import Users, user_schema, users_schema
from app import db
from app.utils.responses import m_return
import app.utils.responses as resp



class UserModel:
    
    @staticmethod
    def create(firstName, lastName, email, password, phoneNumber, location, user_role='user'):
        user = Users(firstName=firstName, lastName=lastName, email=email,password=password, phoneNumber=phoneNumber, location=location,user_role=user_role)
        
        db.session.add(user)
        db.session.commit()
        
        return user
    
    @staticmethod
    def get_all():
        users = Users.query.all()
        
        result = users_schema.jsonify(users)
        
        return result
    
    @classmethod
    def get_one(cls, id):
        
        user = Users.query.filter_by(id=id).first()
        
        if not user:
            return m_return(http_code=resp.USER_DOES_NOT_EXIST['http_code'],
                        message=resp.USER_DOES_NOT_EXIST['message'],
                        code=resp.USER_DOES_NOT_EXIST['code'])
        
        result = user_schema.jsonify(user)
        
        return result
    
    @staticmethod
    def get_admin():
        
        user_role = 'admin'
    
        employe = Users.query.filter_by(user_role=user_role).all()
        
        result = users_schema.jsonify(employe)
        
        return result
    
    @classmethod
    def promote_user(cls, id, user_role):
        
        admin = Users.query.get_or_404(id)
    
        admin.user_role = user_role
    
        if user_role == 'super_admin' or user_role == 'admin' :
        
            admin.user_role = user_role
    
        
        db.session.commit()
        
        return user_schema.jsonify(admin), 200
        
        
        