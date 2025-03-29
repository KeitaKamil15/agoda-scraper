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
    SQLAlchemy Bookmark model representing hotel bookmarks with comparison data from both platforms.
    """
    __tablename__ = "bookmarks"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    hotel_name = Column(String, nullable=False)
    hotel_location = Column(String, nullable=False)
    
    # Booking.com data
    booking_price = Column(Integer, nullable=True)
    booking_url = Column(String, nullable=True)
    booking_image = Column(String, nullable=True)
    booking_alt = Column(String, nullable=True)
    
    # Agoda data
    agoda_price = Column(Integer, nullable=True)
    agoda_url = Column(String, nullable=True)
    agoda_image = Column(String, nullable=True)
    
    # Common data
    star_rating = Column(Integer, nullable=False)
    best_platform = Column(String, nullable=False)
    city = Column(String, nullable=False)
    price_range = Column(String, nullable=True)
    
    # Relationship to user
    user = relationship("User", back_populates="bookmarks")