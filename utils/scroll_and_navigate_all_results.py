"""
Continuously scrolls down the page and clicks 'Next' when available
to load all hotel listings across multiple pages. Extracts hotel information
that matches the specified criteria.

Args:
    page: The Playwright page object
    city_name: The city being searched
    star_rating: The target star rating to filter by (e.g., "5", "4", "3")
    min_price: The minimum price to filter by (optional)
    max_price: The maximum price to filter by (optional)
    
Returns:
    list: List of dictionaries containing hotel information
"""   


from .helper_methods import get_dates, random_delay, simulate_human_mouse
import random
from tqdm import tqdm

from .extract_hotel_info import extract_hotel_info


def scroll_and_navigate_all_results(page, city_name, star_rating, min_price=None, max_price=None):
    hotel_info = [] 
    page_num = 1
    
    while True:
        # Wait for the content container to load
        page.wait_for_selector('//div[@id="contentContainer"]', timeout=10000)
        print(f"Page {page_num} loaded. Scrolling through results...")

        # Check if search results are empty after setting price filters
        no_results_xpath = "//*[@id='contentContainer']//p[contains(text(), \"We couldn't find any results that match your search criteria\")]"

        try:
            page.wait_for_selector(no_results_xpath, timeout=5000)
            print("No results found anymore.")
        except:
            pass

        # Scroll down gradually to load all hotels on current page
        last_height = page.evaluate("document.body.scrollHeight")
        current_position = 0
        
        while current_position < last_height:
            # Calculate scroll amount as a percentage of the remaining page
            remaining_height = last_height - current_position
            # Scroll between 15-25% of the remaining height
            scroll_percentage = random.uniform(0.15, 0.25)
            scroll_amount = int(remaining_height * scroll_percentage)
            
            # Ensure we scroll at least a little bit
            scroll_amount = max(scroll_amount, 200)
            
            # Perform the scroll
            page.evaluate(f"window.scrollBy(0, {scroll_amount})")
            current_position += scroll_amount
            
            random_delay(0.5, 1.5)  # Small pause between scrolls
            
            # Check if content has dynamically loaded and increased page height
            new_height = page.evaluate("document.body.scrollHeight")
            if new_height > last_height:
                last_height = new_height
        
        print("Extracting hotel details from current page...")
        hotel_items = page.query_selector_all("//*[@id='contentContainer']//ol[@class='hotel-list-container']//li[@data-selenium='hotel-item']")
        
        for item in tqdm(hotel_items, desc=f"Processing page {page_num}"):
            hotel_data = extract_hotel_info(item, star_rating, min_price, max_price)
            if hotel_data:
                hotel_info.append(hotel_data)
                print(f"Added hotel: {hotel_data['hotel_name']} (${hotel_data['hotel_price']}, {hotel_data['hotel_rating']} stars)")
        
        print(f"Extracted {len(hotel_info)} matching hotels so far.")
        
        # Check if "Next" button exists
        next_button_visible = page.is_visible('//*[@id="paginationNext"]')
        if not next_button_visible:
            print("No 'Next' button found. Reached the last page of listings.")
            break
        
        # Click the Next button to go to the next page
        simulate_human_mouse(page)  # Simulate human mouse movement
        print(f"Clicking 'Next' to navigate to page {page_num + 1}...")
        page.click('//*[@id="paginationNext"]')
        
        random_delay(4, 5)  # Wait for the next page to load
        page_num += 1
    
    print(f"Finished navigating through all {page_num} pages of hotel listings.")
    print(f"Total hotels extracted: {len(hotel_info)}")
    random_delay(1, 3)
    
    return hotel_info