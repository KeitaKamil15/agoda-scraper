from bs4 import BeautifulSoup
import json
from pathlib import Path
import re
from typing import List, Dict

def filter_hotels(hotels: List[Dict], min_price: int, max_price: int, min_rating: int) -> List[Dict]:
    """Filters hotels based on price range and minimum rating."""
    return [
        hotel for hotel in hotels
        if min_price <= hotel["price"] <= max_price and hotel["star_rating"] == min_rating
    ]

def extract_hotel_data(file_path: str) -> list[dict]:
    """Extracts hotel image 'src' and 'alt' attributes, hotel names, booking prices, booking URLs, and star ratings from the given HTML file."""
    file_content = Path(file_path).read_text(encoding="utf-8")
    soup = BeautifulSoup(file_content, "html.parser")
    
    hotels = soup.select('#bodyconstraint-inner div[data-testid="property-card-container"]')
    
    extracted_hotels = []
    for hotel in hotels:
        img = hotel.select_one('img')
        title = hotel.select_one('div[data-testid="title"]')
        price_element = hotel.select_one('span[data-testid="price-and-discounted-price"]')
        booking_link = hotel.select_one('a[data-testid="availability-cta-btn"]')
        rating_element = hotel.select_one('div[aria-label$="out of 5"]')
        
        price_text = price_element.get_text(strip=True) if price_element else ""
        price_match = re.search(r'\d+', price_text.replace(',', ''))
        price = int(price_match.group()) if price_match else None
        
        rating_text = rating_element.get("aria-label", "") if rating_element else ""
        rating_match = re.search(r'(\d) out of 5', rating_text)
        rating = int(rating_match.group(1)) if rating_match else None
        
        if rating is not None:
            hotel_data = {
                "title": title.get_text(strip=True) if title else "",
                "price": price,
                "booking_url": booking_link.get("href", "") if booking_link else "",
                "star_rating": rating,
                "hotel_img": {
                    "src": img.get("src", "") if img else "",
                    "alt": img.get("alt", "") if img else ""
                }
            }
            extracted_hotels.append(hotel_data)
    
    return extracted_hotels


# Example usage
if __name__ == "__main__":
    file_path = "html_files/dhaka.html"  
    hotel_data = extract_hotel_data(file_path)

    min_price = 100000  # Example min price
    max_price = 1000000  # Example max price
    min_rating = 4    # Example minimum rating
    
    filtered_hotels = filter_hotels(hotel_data, min_price, max_price, min_rating)
    #save the extracted data in a json file
    with open("jsons/hotel_info.json", "w", encoding="utf-8") as f:
        json.dump(filtered_hotels, f, indent=2)
