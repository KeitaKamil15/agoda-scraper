from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
from app.database import get_db
from app.models import Bookmark, User
from pydantic import BaseModel
from fastapi.templating import Jinja2Templates
from typing import Optional

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

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

@router.post("/bookmark")
def create_bookmark(
    bookmark_data: BookmarkCreate, 
    request: Request, 
    db: Session = Depends(get_db)
):
    # Check if user is logged in
    email = request.session.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Check if bookmark already exists
    existing_bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user.id, 
        Bookmark.hotel_name == bookmark_data.hotel_name
    ).first()
    
    if existing_bookmark:
        return {"status": "already_bookmarked"}
    
    # Retrieve search parameters from session
    search_params = request.session.get('search_params', {})
    
    # Create new bookmark
    new_bookmark = Bookmark(
        user_id=user.id,
        hotel_name=bookmark_data.hotel_name,
        hotel_location=bookmark_data.hotel_location,
        booking_price=bookmark_data.booking_price,
        booking_url=bookmark_data.booking_url,
        booking_image=bookmark_data.booking_image,
        booking_alt=bookmark_data.booking_alt,
        agoda_price=bookmark_data.agoda_price,
        agoda_url=bookmark_data.agoda_url,
        agoda_image=bookmark_data.agoda_image,
        star_rating=bookmark_data.star_rating,
        best_platform=bookmark_data.best_platform,
        city=search_params.get('city', 'Unknown'),
        price_range=f"{search_params.get('min_price', 0)}-{search_params.get('max_price', 0)}",
    )
    
    db.add(new_bookmark)
    db.commit()
    db.refresh(new_bookmark)
    
    return {"status": "bookmarked"}

@router.get("/bookmarks")
def get_bookmarks(request: Request, db: Session = Depends(get_db)):
    # Check if user is logged in
    email = request.session.get("email")
    username = request.session.get("user")
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Get user's bookmarks
    bookmarks = db.query(Bookmark).filter(Bookmark.user_id == user.id).all()
    
    return templates.TemplateResponse("bookmarks.html", {
        "request": request, 
        "bookmarks": bookmarks,
        "username": username
    })

@router.delete("/bookmark/{hotel_name}")
def delete_bookmark(
    hotel_name: str, 
    request: Request, 
    db: Session = Depends(get_db)
):
    # Check if user is logged in
    email = request.session.get("email")
    if not email:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    # Find the user
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Find and delete the bookmark
    bookmark = db.query(Bookmark).filter(
        Bookmark.user_id == user.id, 
        Bookmark.hotel_name == hotel_name
    ).first()
    
    if not bookmark:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    
    db.delete(bookmark)
    db.commit()
    
    return {"status": "bookmark_deleted"}