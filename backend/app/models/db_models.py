"""SQLAlchemy ORM Models."""

from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, JSON
from sqlalchemy.sql import func
from app.database.database import Base


class Trip(Base):
    __tablename__ = "trips"
    id = Column(Integer, primary_key=True, index=True)
    user_session = Column(String, index=True, default="demo")
    name = Column(String, nullable=False)
    destination = Column(String, nullable=False)
    days = Column(Integer, nullable=False)
    group_size = Column(Integer, default=1)
    budget = Column(Float, nullable=False)
    status = Column(String, default="active")
    ml_results = Column(JSON, nullable=True)
    itinerary = Column(JSON, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())


class Favourite(Base):
    __tablename__ = "favourites"
    id = Column(Integer, primary_key=True, index=True)
    user_session = Column(String, index=True, default="demo")
    item_type = Column(String, default="destination")  # destination | place
    item_id = Column(String, nullable=False)
    item_name = Column(String, nullable=False)
    item_image = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


class Destination(Base):
    __tablename__ = "destinations"
    id = Column(Integer, primary_key=True, index=True)
    destination = Column(String, unique=True, index=True)
    country = Column(String, default="India")
    region = Column(String, nullable=True)
    image = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    avg_rating = Column(Float, default=4.0)
    avg_cost_per_day = Column(Float, default=3000)
    best_duration_days = Column(Integer, default=3)
    categories = Column(JSON, nullable=True)
    best_season = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
