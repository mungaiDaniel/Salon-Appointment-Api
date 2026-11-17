"""Reusable SQLAlchemy model mixins."""

from datetime import datetime, timezone

from sqlalchemy import Column, DateTime, String

from app.database.database import db


def _utcnow() -> datetime:
    return datetime.now(timezone.utc).replace(tzinfo=None)


class AuditMixin:
    """Adds creation/update timestamps and a ``created_by`` marker, plus ``save()``."""

    date_created = Column(DateTime, nullable=False, default=_utcnow)
    date_updated = Column(DateTime, nullable=False, default=_utcnow, onupdate=_utcnow)
    created_by = Column(String(100), nullable=False, default="SYSTEM")

    def save(self) -> None:
        db.session.add(self)
        db.session.commit()
