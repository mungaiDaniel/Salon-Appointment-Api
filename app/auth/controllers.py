from app.auth.model import User
from app.database.model import user_schema


class UserController:
    model = User
    schema = user_schema

    @classmethod
    def create_user(cls, data, session):
        
        password = User.generate_password_hash(data.get('password'))
        
        user = cls.model(
            firstName=data.get('firstName'),
            lastName=data.get('lastName'),
            email=data.get('email'),
            password=password,
            user_role= "user",
            phoneNumber=data.get('phoneNumber'),
            location=data.get('location'),
            created_by="SYSTEM"
        )
        
        cls.model.save(user, session=session)
        return user_schema.jsonify(user)
