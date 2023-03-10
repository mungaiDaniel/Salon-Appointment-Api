import datetime
from sqlalchemy import Column, DateTime, String, Boolean
from sqlalchemy.orm import declarative_base

from exceptions import DatabaseError
from app import db
from app.utils.responses import m_return
import app.utils.responses as resp
import logging


class BaseModel(object):
    """Base model class

    Args:
        object (_type_): class to hold repetative fields and methods
    """

    __abstract__ = True

    date_created = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.now
    )
    date_updated = Column(
        DateTime(timezone=True), nullable=False, default=datetime.datetime.now
    )
    created_by = Column(String(100), nullable=False, default="SYSTEM")
    active = Column(Boolean, nullable=False, default=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def save(self, session):
        """Save record to database

        Args:
            session (_type_): database session
        """
        try:
            session.add(self)
            session.commit()
        except Exception as exc:
            # session.rollback()
            raise DatabaseError("problem saving record to database")

    def set_model_dict(self, model_dict):
        """Create a model from a dictionary data

        Args:
            model_dict (_type_): data in a dict
        """

        for k, v in model_dict.items():
            getattr(self, k, setattr(self, k, v))

    def get_all(self, session):
        items = session.query(self).all()
        return items

    def get_one(self, id, session):

        try:
            items = session.query(self).get(id)

        except Exception as why:

            print('No user found by that id' + str(why))

            return None

        return items


Base = declarative_base(cls=BaseModel)
