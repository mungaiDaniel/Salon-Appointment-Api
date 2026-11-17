from app.database.database import db
from app.database.mixins import AuditMixin


class Bookings(AuditMixin, db.Model):
    __tablename__ = "bookings"
    __table_args__ = (db.UniqueConstraint("employee_id", "date", name="uq_booking_employee_slot"),)

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, nullable=False)
    employee_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
