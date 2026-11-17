from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.auth.model import User
from app.bookings.model import Bookings
from app.database.database import db
from app.errors import conflict, forbidden, not_found
from app.service.model import Services


class BookingController:
    @staticmethod
    def book(data: dict, user: User) -> Bookings:
        if db.session.get(Services, data["service_id"]) is None:
            raise not_found("Service not found.", code="service_not_found")

        employee_id = data["employee_id"]
        if employee_id is not None and db.session.get(User, employee_id) is None:
            raise not_found("Employee not found.", code="employee_not_found")

        if employee_id is not None:
            taken = db.session.execute(
                select(Bookings.id).filter_by(employee_id=employee_id, date=data["date"])
            ).first()
            if taken:
                raise conflict(
                    "That employee is already booked at that time.", code="slot_unavailable"
                )

        booking = Bookings(
            date=data["date"],
            employee_id=employee_id,
            service_id=data["service_id"],
            user_id=user.id,
            created_by=str(user.id),
        )
        try:
            booking.save()
        except IntegrityError:  # lost a race against a concurrent booking for the same slot
            db.session.rollback()
            raise conflict("That employee is already booked at that time.", code="slot_unavailable")
        return booking

    @staticmethod
    def list_for(user: User) -> list[Bookings]:
        """Admins see every booking; customers only their own."""
        query = select(Bookings).order_by(Bookings.date)
        if user.role_level < 1:
            query = query.filter_by(user_id=user.id)
        return list(db.session.execute(query).scalars())

    @staticmethod
    def get_for(booking_id: int, user: User) -> Bookings:
        booking = db.session.get(Bookings, booking_id)
        if booking is None:
            raise not_found("Booking not found.", code="booking_not_found")
        if booking.user_id != user.id and user.role_level < 1:
            raise forbidden()
        return booking
