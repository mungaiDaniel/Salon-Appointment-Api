from datetime import datetime
from app.bookings.model import Bookings
from app.schemas.schemas import booking_schema, bookings_schemas
from flask_jwt_extended import get_jwt_identity
from app.auth.model import User
from app.service.model import Services
from flask import jsonify, make_response


class BookingController:

    model = Bookings

    @classmethod
    def book_appointment(cls, data, session):

        identity = get_jwt_identity()
        if isinstance(identity, dict):
            email = identity.get("email")
        else:
            email = identity

        user = User.query.filter_by(email=email).first() if email else None
        if not user and data.get("user_id"):
            user = User.query.filter_by(id=data.get("user_id")).first()

        if not user:
            return make_response(jsonify({"message": "User not found"}), 404)

        employee = data.get("employee_id")
        employee_obj = User.query.filter_by(id=employee).first() if employee else user

        service = data.get("service_id")
        service_obj = Services.query.filter_by(id=service).first()
        if not service_obj:
            return make_response(jsonify({"message": "Service not found"}), 404)

        booking_date = data.get("date")
        if isinstance(booking_date, str):
            try:
                booking_date = datetime.fromisoformat(booking_date)
            except ValueError:
                try:
                    booking_date = datetime.strptime(booking_date, "%Y-%m-%d %H:%M:%S")
                except ValueError:
                    booking_date = datetime.strptime(booking_date, "%Y-%m-%d")

        bookings = cls.model(
            date=booking_date,
            employee_id=employee_obj.id if employee_obj else user.id,
            service_id=service_obj.id,
            user_id=user.id,
        )
        cls.model.save(bookings, session=session)

        return booking_schema.dump(bookings), 201

    @classmethod
    def get_all_bookings(cls, session):
        book = Bookings.get_all(cls.model, session)

        return bookings_schemas.dump(book)

    @classmethod
    def get_booking_by_id(cls, id, session):

        book = Bookings.get_one(cls.model, id, session)

        return book
