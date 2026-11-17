from flask import Blueprint, current_app, jsonify, request
from flask_jwt_extended import current_user, get_jwt_identity, jwt_required, verify_jwt_in_request

from app.auth.controllers import UserController
from app.errors import forbidden
from app.extensions import limiter
from app.schemas.schemas import (
    load_json,
    login_schema,
    public_employees_schema,
    register_schema,
    user_schema,
    users_schema,
)
from app.utils.decorators import role_required

user_v1 = Blueprint("user_v1", __name__, url_prefix="/api/v1")


@user_v1.route("/users", methods=["POST"])
@limiter.limit(lambda: current_app.config["RATELIMIT_REGISTER"])
def add_user():
    data = load_json(register_schema, request.get_json(silent=True))
    return jsonify(user_schema.dump(UserController.create_user(data))), 201


@user_v1.route("/users", methods=["GET"])
@role_required("admin")
def get_all():
    return jsonify(users_schema.dump(UserController.list_users()))


@user_v1.route("/users/<int:id>", methods=["GET"])
@jwt_required()
def get_one(id):
    """Admins may read any profile; everyone else only their own."""
    if current_user.id != id and current_user.role_level < 1:
        raise forbidden()
    return jsonify(user_schema.dump(UserController.get_user(id)))


@user_v1.route("/login", methods=["POST"])
@limiter.limit(lambda: current_app.config["RATELIMIT_LOGIN"])
def login():
    data = load_json(login_schema, request.get_json(silent=True))
    result = UserController.authenticate(data["email"], data["password"])
    return jsonify({"code": "ok", "message": "SUCCESS.", "value": result}), 200


@user_v1.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    return jsonify(
        {"code": "ok", "message": "SUCCESS.", "value": UserController.refresh(current_user)}
    )


@user_v1.route("/super_admin/<int:id>", methods=["PUT"])
@role_required("super_admin")
def promote_super_admin(id):
    return jsonify(user_schema.dump(UserController.set_role(id, "super_admin")))


@user_v1.route("/admin/<int:id>", methods=["PUT"])
@role_required("super_admin")
def promote_admin(id):
    return jsonify(user_schema.dump(UserController.set_role(id, "admin")))


@user_v1.route("/employees", methods=["GET"])
def employees():
    """Public staff list for the booking page; contact details only for admin callers."""
    staff = UserController.list_staff()
    verify_jwt_in_request(optional=True)
    if get_jwt_identity() and current_user and current_user.role_level >= 1:
        return jsonify(users_schema.dump(staff))
    return jsonify(public_employees_schema.dump(staff))
