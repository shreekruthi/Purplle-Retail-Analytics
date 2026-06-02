from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import (
    Column,
    String,
    Boolean,
    Float,
    BigInteger,
    DateTime,
    JSON
)

from datetime import datetime


class Base(DeclarativeBase):
    pass


class EventRow(Base):

    __tablename__ = "events"

    event_id = Column(String, primary_key=True)

    store_id = Column(String, nullable=False)

    camera_id = Column(String, nullable=False)

    visitor_id = Column(String, nullable=False)

    event_type = Column(String, nullable=False)

    zone_id = Column(String)

    dwell_ms = Column(BigInteger, default=0)

    is_staff = Column(Boolean, default=False)

    confidence = Column(Float)

    timestamp = Column(DateTime)

    metadata_json = Column(JSON)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )
from sqlalchemy import Integer


class SessionRow(Base):

    __tablename__ = "sessions"

    session_id = Column(
        String,
        primary_key=True
    )

    store_id = Column(
        String,
        nullable=False
    )

    visitor_id = Column(
        String,
        nullable=False
    )

    entry_time = Column(DateTime)

    exit_time = Column(DateTime)

    converted = Column(
        Boolean,
        default=False
    )

    is_staff = Column(
        Boolean,
        default=False
    )

    total_dwell_ms = Column(
        BigInteger,
        default=0
    )

    zones_visited = Column(
        JSON,
        default=list
    )