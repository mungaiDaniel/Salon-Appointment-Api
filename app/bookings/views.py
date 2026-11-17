from flask import Blueprint, jsonify, request
from flask_jwt_extended import current_user, jwt_required

from app.bookings.controllers import BookingController
from app.schemas.schemas import booking_input_schema, booking_schema, bookings_schema, load_json

booking_v1 = Blueprint("booking_v1", __name__, url_prefix="/api/v1")


@booking_v1.route("/booking", methods=["POST"])
@jwt_required()
def book():
    data = load_json(booking_input_schema, request.get_json(silent=True))
    return jsonify(booking_schema.dump(BookingController.book(data, current_user))), 201


@booking_v1.route("/booking", methods=["GET"])
@jwt_required()
def get_all_bookings():
    return jsonify(bookings_schema.dump(BookingController.list_for(current_user)))


@booking_v1.route("/booking/<int:id>", methods=["GET"])
@jwt_required()
def get_one_booking(id):
    return jsonify(booking_schema.dump(BookingController.get_for(id, current_user)))
