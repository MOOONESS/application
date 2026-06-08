from sqlalchemy import Column, Integer, String, Float, ForeignKey, Text, TIMESTAMP
from sqlalchemy.sql import func
from database import Base

class Place(Base):
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(Text)
    category = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)
    image_url = Column(Text, nullable=True)
    created_at = Column(TIMESTAMP, server_default=func.now())


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    email = Column(String)
    password_hash = Column(Text)


class Itinerary(Base):
    __tablename__ = "itineraries"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)


class ItineraryPoint(Base):
    __tablename__ = "itinerary_points"

    id = Column(Integer, primary_key=True)
    itinerary_id = Column(Integer, ForeignKey("itineraries.id"))
    place_id = Column(Integer, ForeignKey("places.id"))
    order_index = Column(Integer)

class Hotel(Base):
    __tablename__ = "hotels"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)
    rating = Column(Float)
    zone_id = Column(Integer, ForeignKey("places.id"))

class Restaurant(Base):
    __tablename__ = "restaurants"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    cuisine = Column(String)
    price = Column(Float)
    zone_id = Column(Integer, ForeignKey("places.id"))

class Museum(Base):
    __tablename__ = "museums"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    ticket_price = Column(Float)
    zone_id = Column(Integer, ForeignKey("places.id"))

# class Zone(Base):
#     __tablename__ = "places"
#     id = Column(Integer, primary_key=True, index=True)
#     name = Column(String)