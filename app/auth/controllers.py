from typing import Optional

from app.auth.model import User
from app.schemas.schemas import user_schema, users_schema
from app.database.database import db
from flask import jsonify, make_response
from flask_jwt_extended import create_refresh_token
from exceptions import AuthenticationError
import app.utils.responses as resp


# Role-to-permission-level mapping used by token generation.
_ROLE_PERMISSION: dict[str, int] = {
    "user": 0,
    "admin": 1,
    "super_admin": 2,
}


class UserController:
    model = User

    @classmethod
    def authenticate(cls, email: str, password: str) -> dict:
        """Authenticate a user by email/password and return token payload.

        Returns:
            dict with keys: access_token, refresh_token, user_role, user.

        Raises:
            AuthenticationError: on missing user, bad password, or unknown role.
        """
        user = User.query.filter_by(email=email).first()

        if user is None:
            raise AuthenticationError(
                http_code=resp.USER_DOES_NOT_EXIST["http_code"],
                message=resp.USER_DOES_NOT_EXIST["message"],
                code=resp.USER_DOES_NOT_EXIST["code"],
            )

        if not user.verify_password_hash(password):
            raise AuthenticationError(
                http_code=resp.CREDENTIALS_ERROR_999["http_code"],
                message=resp.CREDENTIALS_ERROR_999["message"],
                code=resp.CREDENTIALS_ERROR_999["code"],
            )

        permission_level = _ROLE_PERMISSION.get(user.user_role)
        if permission_level is None:
            raise AuthenticationError(
                http_code=resp.PERMISSION_DENIED["http_code"],
                message=resp.PERMISSION_DENIED["message"],
                code=resp.PERMISSION_DENIED["code"],
            )

        access_token: str = user.generate_auth_token(permission_level)
        refresh_token: str = create_refresh_token(identity={"email": email})

        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user_role": user.user_role,
            "user": user.firstName,
        }

    @classmethod
    def create_user(cls, data: dict, session) -> tuple:

        password = User.generate_password_hash(data.get("password"))

        user = cls.model(
            firstName=data.get("firstName"),
            lastName=data.get("lastName"),
            email=data.get("email"),
            password=password,
            user_role="user",
            phoneNumber=data.get("phoneNumber"),
            location=data.get("location"),
            created_by="SYSTEM",
        )

        if session.query(User.query.filter(User.email == user.email).exists()).scalar():

            return make_response(
                jsonify({"status": 409, "message": "user with that email already exists"}), 409
            )

        cls.model.save(user, session=session)

        return user_schema.dump(user), 201

    @staticmethod
    def get_admin() -> list:
        user_role = "super_admin"
        employe = User.query.filter_by(user_role=user_role).all()
        result = users_schema.dump(employe)

        return result

    @classmethod
    def promote_user(cls, id: int, session) -> Optional[tuple]:

        user_role = "super_admin"

        admin = User.get_one(cls.model, id, session)

        if admin is None:
            return

        admin.user_role = user_role

        db.session.commit()

        return user_schema.dump(admin), 200

    @classmethod
    def user_admin(cls, id: int, session) -> Optional[tuple]:

        user_role = "admin"

        admin = User.get_one(cls.model, id, session)

        if admin is None:
            return

        admin.user_role = user_role

        db.session.commit()

        return user_schema.dump(admin), 200

    @classmethod
    def get_user_by_id(cls, id: int, session) -> Optional[User]:
        user = User.get_one(cls.model, id, session)

        if user is None:

            return
        return user

    @classmethod
    def get_all_users(cls, session) -> tuple:
        users = User.get_all(cls.model, session)

        return users_schema.dump(users), 200
