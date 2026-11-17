from sqlalchemy import select

from app.database.database import db
from app.errors import not_found
from app.service.model import Services


class ServiceController:
    @staticmethod
    def create(data: dict, creator_id: int) -> Services:
        service = Services(**data, user_id=creator_id, created_by=str(creator_id))
        service.save()
        return service

    @staticmethod
    def list_all() -> list[Services]:
        return list(db.session.execute(select(Services).order_by(Services.id)).scalars())

    @staticmethod
    def get(service_id: int) -> Services:
        service = db.session.get(Services, service_id)
        if service is None:
            raise not_found("Service not found.", code="service_not_found")
        return service

    @classmethod
    def update(cls, service_id: int, data: dict) -> Services:
        service = cls.get(service_id)
        for field, value in data.items():
            setattr(service, field, value)
        db.session.commit()
        return service

    @classmethod
    def delete(cls, service_id: int) -> None:
        db.session.delete(cls.get(service_id))
        db.session.commit()
