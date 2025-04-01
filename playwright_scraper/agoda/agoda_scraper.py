import time
import random
import json
from playwright.sync_api import sync_playwright
from helper_methods import get_dates, random_delay, simulate_human_mouse
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
import os
from tqdm import tqdm

# Define user-agents specific to each browser
with open('user_agents.json') as f:
    USER_AGENTS = json.load(f)

def visit_agoda_homepage(p):
    """
    Initializes the browser, context, and page. Navigates to the Booking.com homepage 
    with human-like behavior. Returns the tuple (page, context, browser) for further actions.
    """
    # Randomly choose a browser
    browser_name = random.choice(["firefox"])
    print(f"Using browser: {browser_name}")
    # Pick a random user agent for the selected browser
    user_agent = random.choice(USER_AGENTS[browser_name])
    user_agent = USER_AGENTS[browser_name][0]
    print(f"Using user agent: {user_agent}")
    # Launch the chosen browser
    browser = getattr(p, browser_name).launch(headless=False)
    # Create a new browser context with the selected user-agent
    context = browser.new_context(
        user_agent=user_agent,
        viewport={'width': 1280, 'height': 800},
        locale='en-US'
    )
    # Disable WebDriver flag to bypass bot detection
    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    # Open a new page in the context
    page = context.new_page()
    # Navigate to Booking.com homepage
    page.goto("https://www.agoda.com/", wait_until="networkidle")
    random_delay(1, 3)
    # Mimic a small scroll to emulate human behavior
    page.evaluate("window.scrollBy(0, window.innerHeight/8)")
    random_delay(1, 2)
    return page, context, browser

def search_agoda_homepage(page, city_name: str):
    """
    Performs the homepage search by entering the city name, selecting check-in and check-out dates,
    and clicking the search button.
    """
    # Fill in the search field
    page.type("xpath=//*[@id='textInput']", city_name, delay=random.randint(50, 150))
    random_delay(1, 2)
    print(f"Entered city name: {city_name}")
    
    # Click at the top-left corner to dismiss the suggestions dropdown
    page.mouse.click(10, 10)  # Coordinates near top-left corner
    random_delay(0.5, 1)
    print("Clicked to dismiss suggestions dropdown")
    
    # Get tomorrow and day after tomorrow's dates
    check_in_date, check_out_date = get_dates()
    
    # Click on check-in box to open the date picker
    page.click("xpath=//*[@id='check-in-box']")
    random_delay(1, 2)
    print(f"Clicked check-in box, selecting date: {check_in_date}")
    
    # Click on the check-in date
    page.click(f"xpath=//span[@data-selenium-date='{check_in_date}']")
    random_delay(1, 2)
    print(f"Selected check-in date: {check_in_date}")
    
    # Automatically selects check-out date after check-in, but in case we need to explicitly select it:
    page.click(f"xpath=//span[@data-selenium-date='{check_out_date}']")
    random_delay(1, 2)
    print(f"Selected check-out date: {check_out_date}")
    
    # Click at the top-left corner to dismiss the date picker if needed
    page.mouse.click(10, 10)
    random_delay(0.5, 1)
    print("Clicked to dismiss date picker")
    
    # Simulate human mouse movement before clicking the search button
    simulate_human_mouse(page)
    page.click("xpath=//*[@id='Tabs-Container']/button//span[contains(text(),'SEARCH')]")
    random_delay(2, 3)
    print("Clicked search button...")

def apply_hotel_filter(page, star_rating, min_price=None, max_price=None):
    """
    Clicks on the star rating filter checkbox and sets price range filters.
    
    Args:
        page: The Playwright page object
        star_rating: The star rating to filter by (e.g., "5", "4", "3")
        min_price: The minimum price to filter by (optional)
        max_price: The maximum price to filter by (optional)
        
    Returns:
        bool: True if search results are available after filtering, False otherwise
    """
    # Wait for the filter section to be visible
    page.wait_for_selector('//*[@id="SideBarLocationFilters"]', timeout=10000)
    
    # Apply price filters if provided
    if min_price is not None:
        min_price_xpath = '//div[@id="SideBarLocationFilters"]//input[@id="price_box_0"][@aria-label="Minimum price filter"]'
        # Clear the existing value first (select all text and delete)
        page.click(min_price_xpath)
        page.keyboard.press("Control+A")
        page.keyboard.press("Delete")
        
        # Type the new minimum price
        page.type(min_price_xpath, str(min_price), delay=random.randint(50, 150))
        random_delay(0.5, 1)
        print(f"Set minimum price filter to {min_price}")
    
    if max_price is not None:
        max_price_xpath = '//div[@id="SideBarLocationFilters"]//input[@id="price_box_1"][@aria-label="Maximum price filter"]'
        # Clear the existing value first (select all text and delete)
        page.click(max_price_xpath)
        page.keyboard.press("Control+A")
        page.keyboard.press("Delete")
        
        # Type the new maximum price
        page.type(max_price_xpath, str(max_price), delay=random.randint(50, 150))
        random_delay(0.5, 1)
        print(f"Set maximum price filter to {max_price}")
    
    # Apply price filters by pressing Enter if either min or max was set
    if min_price is not None or max_price is not None:
        page.keyboard.press("Enter")
        random_delay(2, 3)
        print("Applied price filters")
        
        # Check if search results are empty after setting price filters
        no_results_xpath = "//*[@id='contentContainer']//p[contains(text(), \"We couldn't find any results that match your search criteria\")]"
        if page.is_visible(no_results_xpath, timeout=5000):
            print("No results found after setting price filters.")
            return False
    
    page.mouse.click(10, 10)  # Coordinates near top-left corner
    random_delay(0.5, 1)
    
    # try:
    #     # Construct the filter xpath
    #     filter_xpath = f'//*[@id="SideBarLocationFilters"]//li/label[@data-element-name="search-filter-starratingwithluxury"][@data-element-value="{star_rating}"]'
        
    #     # Click on the star rating filter
    #     # simulate_human_mouse(page)
    #     #scroll down a bit
    #     page.evaluate("window.scrollBy(0, window.innerHeight/2)")
    #     #scroll down 300 more
    #     page.evaluate("window.scrollBy(0, 300)")
    #     random_delay(1, 2)
    #     page.click(filter_xpath)
    #     print(f"Clicked on {star_rating}-star rating filter")
        
    #     # Wait for the page to update with filtered results
    #     random_delay(3, 5)
        
    #     # Check if search results are empty after applying star rating filter
    #     no_results_xpath = "//*[@id='contentContainer']//p[contains(text(), \"We couldn't find any results that match your search criteria\")]"
    #     if page.is_visible(no_results_xpath, timeout=5000):
    #         print("No results found after applying star rating filter.")
    #         return False
        
    #     # Wait for the content container to refresh
    #     page.wait_for_selector('//div[@id="contentContainer"]', timeout=15000)
    # except Exception as e:
    #     print(f"An error occurred while clicking the start rating: {e}")
    #     # return False
    
    return True
    
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
def scroll_and_navigate_all_results(page, city_name, star_rating, min_price=None, max_price=None):
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
    hotel_info = [] 
    page_num = 1
    
    while True:
        # Wait for the content container to load
        page.wait_for_selector('//div[@id="contentContainer"]', timeout=10000)
        print(f"Page {page_num} loaded. Scrolling through results...")

        # Check if search results are empty after setting price filters
        no_results_xpath = "//*[@id='contentContainer']//p[contains(text(), \"We couldn't find any results that match your search criteria\")]"
        if page.is_visible(no_results_xpath, timeout=5000):
            print("No results found anymore")
            break        
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

def agoda_list_scraping(city_name: str = "", star_rating: str = "5", min_price: int = None, max_price: int = None,output_folder: str = 'jsons'):
    """
    Orchestrates the Agoda scraping process with filters for star rating and price range.
    
    Args:
        city_name: The city to search for
        star_rating: The star rating to filter by (e.g., "5", "4", "3")
        min_price: The minimum price to filter by (optional)
        max_price: The maximum price to filter by (optional)
        
    Returns:
        list: List of dictionaries containing hotel information that matches the criteria
    """
    hotel_results = []
    try:
        with sync_playwright() as p:
            # Initialize browser and visit Agoda homepage
            page, context, browser = visit_agoda_homepage(p)
            
            # Perform the search on the homepage
            search_agoda_homepage(page, city_name)
            
            # Wait for the search results to load
            page.wait_for_selector('//div[@id="contentContainer"]', timeout=15000)
            
            # Apply star rating and price filters
            results_found = apply_hotel_filter(page, star_rating, min_price, max_price)
            
            if results_found:
                # Scroll through all pages and navigate using the Next button
                # Also extract hotel information
                hotel_results = scroll_and_navigate_all_results(page, city_name, star_rating, min_price, max_price)
            else:
                hotel_results = []
                print("No results found after applying filters.")
            
            # Close the context and browser
            context.close()
            browser.close()
    except Exception as e:
        print(f"Error during Agoda scraping: {e}")
    
    # Save results to a JSON file
    output_filename = f"{city_name}_{star_rating}star_hotels.json"
    output_filename = os.path.join(output_folder, output_filename)
    with open(output_filename, 'w', encoding='utf-8') as f:
        json.dump(hotel_results, f, indent=4, ensure_ascii=False)
    print(f"Saved {len(hotel_results)} hotel results to {output_filename}")
    
    return hotel_results

if __name__ == "__main__":
    hotels = agoda_list_scraping(
        city_name='dhaka', 
        star_rating="3", 
        min_price=20,  # Example minimum price
        max_price=30,  # Example maximum price
    )
    
    # Print a summary of the results
    if hotels:
        print(f"\nFound {len(hotels)} hotels matching the criteria:")
        for i, hotel in enumerate(hotels[:5], 1):
            print(f"{i}. {hotel['hotel_name']} - ${hotel['hotel_price']} - {hotel['hotel_rating']} stars")
        
        if len(hotels) > 5:
            print(f"...and {len(hotels) - 5} more hotels")