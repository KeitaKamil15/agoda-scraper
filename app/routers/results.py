from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from starlette.responses import RedirectResponse
from starlette.status import HTTP_303_SEE_OTHER
import os, json
from app.routers.result_utils.hotel_info_retriver import extract_hotel_data, filter_hotels
from difflib import SequenceMatcher

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

def similar(a, b):
    """Calculate string similarity ratio between two strings"""
    return SequenceMatcher(None, a.lower(), b.lower()).ratio()

def match_hotels(booking_hotels, agoda_hotels, threshold=0.8):
    """
    Match hotels between booking.com and agoda based on name similarity
    Returns a list of matched hotels and lists of unmatched hotels from both platforms
    """
    matched_hotels = []
    matched_booking_indices = set()
    matched_agoda_indices = set()
    
    # Find matches
    for b_idx, booking_hotel in enumerate(booking_hotels):
        for a_idx, agoda_hotel in enumerate(agoda_hotels):
            if similar(booking_hotel["title"], agoda_hotel["hotel_name"]) >= threshold:
                # Create a comparison record
                hotel_comparison = {
                    "name": booking_hotel["title"],  # Use booking.com name as primary
                    "booking": {
                        "price": booking_hotel["price"],
                        "url": booking_hotel["booking_url"],
                        "image": booking_hotel["hotel_img"]["src"],
                        "alt": booking_hotel["hotel_img"]["alt"]
                    },
                    "agoda": {
                        "price": int(float(agoda_hotel["hotel_price"])) * 120,  # Convert to same currency unit
                        "url": agoda_hotel["booking_url"],
                        "image": "https:" + agoda_hotel["image_url"] if not agoda_hotel["image_url"].startswith("http") else agoda_hotel["image_url"]
                    },
                    "star_rating": booking_hotel["star_rating"],
                    "best_platform": "booking" if booking_hotel["price"] <= int(float(agoda_hotel["hotel_price"])) * 120 else "agoda"
                }
                matched_hotels.append(hotel_comparison)
                matched_booking_indices.add(b_idx)
                matched_agoda_indices.add(a_idx)
                break
    
    # Get unmatched booking.com hotels
    unmatched_booking = [
        {
            "name": hotel["title"],
            "booking": {
                "price": hotel["price"],
                "url": hotel["booking_url"],
                "image": hotel["hotel_img"]["src"],
                "alt": hotel["hotel_img"]["alt"]
            },
            "star_rating": hotel["star_rating"],
            "best_platform": "booking",  # Only on booking
            "agoda": None  # No Agoda data
        }
        for i, hotel in enumerate(booking_hotels) if i not in matched_booking_indices
    ]
    
    # Get unmatched agoda hotels
    unmatched_agoda = [
        {
            "name": hotel["hotel_name"],
            "agoda": {
                "price": int(float(hotel["hotel_price"])) * 120,  # Convert to same currency unit
                "url": hotel["booking_url"],
                "image": "https:" + hotel["image_url"] if not hotel["image_url"].startswith("http") else hotel["image_url"]
            },
            "star_rating": int(hotel["hotel_rating"]) if hotel["hotel_rating"].isdigit() else 0,
            "best_platform": "agoda",  # Only on agoda
            "booking": None  # No Booking.com data
        }
        for i, hotel in enumerate(agoda_hotels) if i not in matched_agoda_indices
    ]
    
    # Combine all results
    all_hotels = matched_hotels + unmatched_booking + unmatched_agoda
    return all_hotels

@router.get("/search-results")
def search_results(request: Request):
    """
    Display search results page with hotel price comparisons
    """
    # Check if the user is logged in
    username = request.session.get("user")
    if not username:
        return RedirectResponse(url="/auth/login", status_code=HTTP_303_SEE_OTHER)
    
    # Retrieve search parameters from session
    search_params = request.session.get('search_params', {})
    city = search_params.get('city', '').lower()
    
    # Get Booking.com results
    try:

        booking_html_file_path = f"app/routers/booking_utils/html_files/{city}_booking.html"
        if os.path.exists(booking_html_file_path):
            booking_search_results = extract_hotel_data(booking_html_file_path)
            booking_search_results = filter_hotels(
                booking_search_results, 
                search_params.get("min_price", 0), 
                search_params.get("max_price", 0), 
                search_params.get("star_rating", 0)
            )
        else:
            booking_search_results = []
    except Exception as e:
        print(f"Error processing Booking.com results: {e}")
        booking_search_results = []
    
    # Get Agoda results
    agoda_hotel_list_path = f"app/routers/agoda_utils/jsons/{search_params.get('city', '')}_{search_params.get('star_rating', 0)}star_hotels.json"
    if os.path.exists(agoda_hotel_list_path):
        with open(agoda_hotel_list_path, 'r') as f:
            agoda_search_results = json.load(f)
    else:
        agoda_search_results = []
    
    # Match and compare hotels from both platforms
    comparison_results = match_hotels(booking_search_results, agoda_search_results)
    
    # Sort results by best price
    # comparison_results.sort(key=lambda x: (
    #     min(
    #         x["booking"]["price"] if x["booking"] else float('inf'),
    #         x["agoda"]["price"] if x["agoda"] else float('inf')
    #     )
    # ))
    
    return templates.TemplateResponse(
        "search_results.html",
        {
            "request": request,
            "username": username,
            "search_results": comparison_results,
            "city": search_params.get('city', 'Unknown'),
        }
    )