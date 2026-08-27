from app.assistances.model import UserServices
from app.schemas.schemas import employee_schema


class UserServicesControll:
    model = UserServices

    @classmethod
    def create_assistanceServices(cls, session, service_id, user_id):
        # validate data

        assistanceServices = cls.model(service_id=service_id, user_id=user_id)
        cls.model.save(assistanceServices, session=session)

        return employee_schema.dump(assistanceServices)
