from pydantic import BaseModel, EmailStr
from typing import Optional

class BookmarkCreate(BaseModel):
    hotel_name: str
    hotel_location: str
    booking_price: Optional[int] = None
    booking_url: Optional[str] = None
    booking_image: Optional[str] = None
    booking_alt: Optional[str] = None
    agoda_price: Optional[int] = None
    agoda_url: Optional[str] = None
    agoda_image: Optional[str] = None
    star_rating: int
    best_platform: str

