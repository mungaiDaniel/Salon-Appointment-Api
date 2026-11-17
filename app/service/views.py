from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user

from app.schemas.schemas import load_json, service_input_schema, service_schema, services_schema
from app.service.controllers import ServiceController
from app.utils.decorators import role_required

service_v1 = Blueprint("service_v1", __name__, url_prefix="/api/v1")


@service_v1.route("/stylings", methods=["POST"])
@role_required("admin")
def add_style():
    data = load_json(service_input_schema, request.get_json(silent=True))
    service = ServiceController.create(data, creator_id=current_user.id)
    return jsonify(service_schema.dump(service)), 201


@service_v1.route("/stylings", methods=["GET"])
def get_styles():
    return jsonify(services_schema.dump(ServiceController.list_all()))


@service_v1.route("/stylings/<int:id>", methods=["GET"])
def one_style(id):
    return jsonify(service_schema.dump(ServiceController.get(id)))


@service_v1.route("/stylings/<int:id>", methods=["PUT"])
@role_required("admin")
def update_style(id):
    data = load_json(service_input_schema, request.get_json(silent=True))
    return jsonify(service_schema.dump(ServiceController.update(id, data)))


@service_v1.route("/stylings/<int:id>", methods=["DELETE"])
@role_required("admin")
def delete_style(id):
    ServiceController.delete(id)
    return jsonify({"code": "ok", "message": "Service deleted."}), 200
