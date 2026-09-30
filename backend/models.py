from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float
from sqlalchemy import DateTime

from .database import Base


class Trip(Base):

    __tablename__ = "trips"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    destination = Column(
        String(150),
        nullable=False
    )

    duration = Column(
        Integer,
        nullable=False
    )

    travellers = Column(
        Integer,
        nullable=False
    )

    budget = Column(
        Float,
        nullable=False
    )

    accommodation = Column(
        String(100),
        nullable=False
    )

    interests = Column(
        String(500),
        nullable=False
    )

    itinerary = Column(
        Text,
        nullable=False
    )

    estimated_cost = Column(
        Float,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )