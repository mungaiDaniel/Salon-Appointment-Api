from app.auth.model import User
from app.auth.model import user_schema, users_schema
from app import db
from flask import jsonify, make_response



class UserController:
    model = User

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
        # if user.email:
        #     return make_response(jsonify({
        #         "status": 409,
        #         "message": "Email already registered"
        #     }), 409)
        
        cls.model.save(user, session=session)
       
        return user_schema.jsonify(user)

    @staticmethod
    def get_admin():
        user_role = 'super_admin'
        employe = User.query.filter_by(user_role=user_role).all()
        result = users_schema.jsonify(employe)

        return result

    @classmethod
    def promote_user(cls, id):

        user_role = "super_admin"

        admin = User.query.get_or_404(id)

        admin.user_role = user_role


        db.session.commit()

        return user_schema.jsonify(admin), 200
    @classmethod
    def user_admin(cls, id):

        user_role = "admin"

        admin = User.query.get_or_404(id)

        admin.user_role = user_role


        db.session.commit()

        return user_schema.jsonify(admin), 200
    @classmethod
    def get_user_by_id(cls, id, session):
        user = User.get_one(cls.model, id, session)
        print('<><><><><>', user)
        if user:

            return user
        
        return make_response(jsonify({
            "status": 404,
            "message": "user doesn't exist"
        }), 404)

    @classmethod
    def get_all_users(cls, session):
        users = User.get_all(cls.model, session)

        return users_schema.jsonify(users)
        
        
