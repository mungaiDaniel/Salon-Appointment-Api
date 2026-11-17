from flask import Blueprint, jsonify
from flask_jwt_extended import current_user

from app.assistances.controllers import UserServicesController
from app.schemas.schemas import (
    employee_service_schema,
    employee_services_schema,
    services_schema,
)
from app.utils.decorators import role_required

assistance_v1 = Blueprint("assistance_v1", __name__, url_prefix="/api/v1")


@assistance_v1.route("/employee/<int:user_id>/<int:service_id>", methods=["POST"])
@role_required("admin")
def add_employee(user_id, service_id):
    link = UserServicesController.assign(user_id, service_id, created_by=str(current_user.id))
    return jsonify(employee_service_schema.dump(link)), 201


@assistance_v1.route("/employee/<int:user_id>", methods=["GET"])
def employee_services(user_id):
    return jsonify(employee_services_schema.dump(UserServicesController.for_employee(user_id)))


@assistance_v1.route("/employee_service/<int:employee_id>", methods=["GET"])
def services_for_employee(employee_id):
    """The full service records an employee can perform (used by the booking page)."""
    return jsonify(services_schema.dump(UserServicesController.services_for_employee(employee_id)))
