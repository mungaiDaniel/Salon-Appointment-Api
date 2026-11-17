from app.database.database import db
from app.database.mixins import AuditMixin


class Services(AuditMixin, db.Model):
    __tablename__ = "services"

    id = db.Column(db.Integer, primary_key=True)
    style = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))
    cost = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer, nullable=False)  # minutes
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
