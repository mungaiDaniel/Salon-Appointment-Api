from app.auth.controllers import UserController
from flask import request, Blueprint
from app.database.database import db
from app.schemas.schemas import user_schema
from app.auth.model import User
import logging
from flask import jsonify, make_response
import app.utils.responses as resp
from app.utils.responses import m_return
from exceptions import AuthenticationError

user_v1 = Blueprint("user_v1", __name__, url_prefix="/api/v1")


@user_v1.route("/users", methods=["POST"])
def add_user():
    data = request.get_json()
    session = db.session
    return UserController.create_user(data, session=session)


@user_v1.route("/users/<int:id>", methods=["GET"])
def get_one(id):
    session = db.session
    result = UserController.get_user_by_id(id, session=session)
    if result:

        return user_schema.dump(result)
    return make_response(jsonify({"status": 404, "message": "user doesn't exist"}), 404)


@user_v1.route("/users", methods=["GET"])
def get_all():
    session = db.session

    return UserController.get_all_users(session=session)


@user_v1.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    try:
        email = data["email"]
        password = data["password"]
    except (KeyError, TypeError) as why:
        logging.warning(f"Login parameters missing or invalid: {why}")
        return m_return(
            http_code=resp.MISSED_PARAMETERS["http_code"],
            message=resp.MISSED_PARAMETERS["message"],
            code=resp.MISSED_PARAMETERS["code"],
        )

    try:
        result = UserController.authenticate(email, password)
    except AuthenticationError as exc:
        return m_return(
            http_code=exc.http_code,
            message=exc.message,
            code=exc.code,
        )

    return m_return(
        http_code=resp.SUCCESS["http_code"],
        message=resp.SUCCESS["message"],
        value=result,
    )


@user_v1.route("/super_admin/<int:id>", methods=["PUT"])
def superAdmin(id):
    session = db.session

    admin = UserController.promote_user(id, session=session)

    if admin is None:
        return make_response(jsonify({"status": 404, "message": "user doesn't exist"}), 404)

    return admin


@user_v1.route("/admin/<int:id>", methods=["PUT"])
def make_assisstance(id):

    session = db.session

    admin = UserController.user_admin(id, session=session)

    if admin is None:
        return make_response(jsonify({"status": 404, "message": "user doesn't exist"}), 404)

    return admin


@user_v1.route("/employees", methods=["GET"])
def Admin():
    results = UserController.get_admin()

    return results

