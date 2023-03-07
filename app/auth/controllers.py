from app.auth.model import User
from app.database.model import user_schema, users_schema
from app import db


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

    @staticmethod
    def get_admin():
        user_role = 'admin'
        employe = User.query.filter_by(user_role=user_role).all()
        result = users_schema.jsonify(employe)

        return result

    @classmethod
    def promote_user(cls, id, user_role):

        admin = User.query.get_or_404(id)

        admin.user_role = user_role

        if user_role == 'super_admin' or user_role == 'admin':
            admin.user_role = user_role

        db.session.commit()

        return user_schema.jsonify(admin), 200
