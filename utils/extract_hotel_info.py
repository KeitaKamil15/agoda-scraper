def extract_hotel_info(item, star_rating, min_price=None, max_price=None):
    """
    Extracts hotel information from a single hotel item element.
    
    Args:
        item: The hotel item element.
        star_rating: The target star rating to match.
        min_price: Minimum price filter.
        max_price: Maximum price filter.
        
    Returns:
        dict or None: A dictionary with hotel details if the hotel matches the criteria, otherwise None.
    """
    try:
        # inner html code in a file
        # with open('app/routers/agoda_utils/item.html', 'w') as f:
        #     f.write(item.inner_html())
        hotel_name_element = item.query_selector("a[data-selenium='hotel-name'] span")
        hotel_name = hotel_name_element.text_content() if hotel_name_element else "N/A"

        if hotel_name == "N/A":
            hotel_name_element = item.query_selector("h3[data-selenium='hotel-name']")
            hotel_name = hotel_name_element.text_content() if hotel_name_element else "N/A"
        
        # Extract hotel rating
        rating_elements = item.query_selector_all("span")
        rating_text = "N/A"
        for element in rating_elements:
            if "stars out of 5" in element.text_content():
                rating_text = element.inner_text()
                break
        
        hotel_rating = "N/A"
        if rating_text != "N/A":
            try:
                hotel_rating = rating_text.split(" ")[0]
            except Exception:
                pass
        
        # Extract hotel price
        price_element = item.query_selector("div[data-element-name='final-price'] span[data-selenium='display-price']")
        price_text = price_element.inner_text() if price_element else "N/A"
        hotel_price = "N/A"
        if price_text != "N/A":
            try:
                hotel_price = float(''.join(c for c in price_text if c.isdigit() or c == '.'))
            except Exception:
                pass
        
        # Extract booking URL
        booking_url_element = item.query_selector("a[data-selenium='hotel-name']")
        booking_url = booking_url_element.get_attribute("href") if booking_url_element else "N/A"
        if booking_url == "N/A":
            booking_url_element = item.query_selector("a[class='PropertyCard__Link']")
            booking_url = booking_url_element.get_attribute("href") if booking_url_element else "N/A"

        # Extract main image URL
        main_image_element = item.query_selector("button[data-element-name='ssrweb-mainphoto'] img")
        main_image_url = main_image_element.get_attribute("src") if main_image_element else "N/A"
        
        # Validate against the provided criteria
        if hotel_rating != "N/A" and hotel_price != "N/A":
            if hotel_rating == star_rating:
                price_in_range = True
                if min_price is not None and hotel_price < min_price:
                    price_in_range = False
                if max_price is not None and hotel_price > max_price:
                    price_in_range = False
                if price_in_range:
                    return {
                        'hotel_name': hotel_name,
                        'hotel_price': hotel_price,
                        'hotel_rating': hotel_rating,
                        'booking_url': 'https://www.agoda.com'+ booking_url,
                        'image_url': 'https:'+ main_image_url
                    }
    except Exception as e:
        print(f"Error extracting hotel information: {e}")
    
    return None