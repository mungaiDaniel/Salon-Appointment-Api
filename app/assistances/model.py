from app.database.database import db
from app.database.mixins import AuditMixin


class UserServices(AuditMixin, db.Model):
    """Links an employee (user) to a service they can perform."""

    __tablename__ = "userservices"
    __table_args__ = (db.UniqueConstraint("user_id", "service_id", name="uq_user_service"),)

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey("services.id"), nullable=False)
