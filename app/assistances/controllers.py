from sqlalchemy import select

from app.assistances.model import UserServices
from app.auth.model import User
from app.database.database import db
from app.errors import conflict, not_found
from app.service.model import Services


class UserServicesController:
    @staticmethod
    def assign(user_id: int, service_id: int, created_by: str) -> UserServices:
        if db.session.get(User, user_id) is None:
            raise not_found("User not found.", code="user_not_found")
        if db.session.get(Services, service_id) is None:
            raise not_found("Service not found.", code="service_not_found")

        existing = db.session.execute(
            select(UserServices.id).filter_by(user_id=user_id, service_id=service_id)
        ).first()
        if existing:
            raise conflict("That service is already assigned to this employee.")

        link = UserServices(user_id=user_id, service_id=service_id, created_by=created_by)
        link.save()
        return link

    @staticmethod
    def for_employee(user_id: int) -> list[UserServices]:
        query = select(UserServices).filter_by(user_id=user_id).order_by(UserServices.id)
        return list(db.session.execute(query).scalars())

    @staticmethod
    def services_for_employee(user_id: int) -> list[Services]:
        query = (
            select(Services)
            .join(UserServices, Services.id == UserServices.service_id)
            .where(UserServices.user_id == user_id)
            .order_by(Services.id)
        )
        return list(db.session.execute(query).scalars())
