from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    """
    SQLAlchemy User model representing users in the database.
    """
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    
    # Relationship to bookmarks
    bookmarks = relationship("Bookmark", back_populates="user")

class Bookmark(Base):
    """
    SQLAlchemy Bookmark model representing hotel bookmarks for users.
    """
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_name = Column(String, nullable=False)
    hotel_location = Column(String, nullable=False)
    hotel_price = Column(Integer, nullable=False)
    hotel_rating = Column(Integer, nullable=False)
    hotel_image_url = Column(String, nullable=False)
    hotel_booking_url = Column(String, nullable=False)
    city = Column(String, nullable=False)
    price_range = Column(String, nullable=False)
    
    # Relationship to user
    user = relationship("User", back_populates="bookmarks")