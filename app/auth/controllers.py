from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import select

from app.auth.model import User
from app.database.database import db
from app.errors import conflict, not_found, unauthorized


class UserController:
    @staticmethod
    def authenticate(email: str, password: str) -> dict:
        """Verify credentials and return the token payload.

        Unknown email and wrong password deliberately produce the *same* error so the
        endpoint cannot be used to discover which emails are registered.
        """
        user = db.session.execute(select(User).filter_by(email=email)).scalar_one_or_none()
        if user is None or not user.verify_password(password):
            raise unauthorized("Invalid email or password.", code="invalid_credentials")

        return {
            "access_token": create_access_token(identity=user.email),
            "refresh_token": create_refresh_token(identity=user.email),
            "user_role": user.user_role,
            "user": user.firstName,
        }

    @staticmethod
    def refresh(user: User) -> dict:
        return {"access_token": create_access_token(identity=user.email)}

    @staticmethod
    def create_user(data: dict) -> User:
        if db.session.execute(select(User.id).filter_by(email=data["email"])).first():
            raise conflict("A user with that email already exists.", code="email_taken")

        user = User(
            firstName=data["firstName"],
            lastName=data["lastName"],
            email=data["email"],
            password=User.generate_password_hash(data["password"]),
            phoneNumber=data["phoneNumber"],
            location=data["location"],
            user_role="user",  # never taken from client input
        )
        user.save()
        return user

    @staticmethod
    def list_users() -> list[User]:
        return list(db.session.execute(select(User).order_by(User.id)).scalars())

    @staticmethod
    def list_staff() -> list[User]:
        query = select(User).where(User.user_role.in_(["admin", "super_admin"])).order_by(User.id)
        return list(db.session.execute(query).scalars())

    @staticmethod
    def get_user(user_id: int) -> User:
        user = db.session.get(User, user_id)
        if user is None:
            raise not_found("User not found.", code="user_not_found")
        return user

    @classmethod
    def set_role(cls, user_id: int, role: str) -> User:
        user = cls.get_user(user_id)
        user.user_role = role
        db.session.commit()
        return user
