import random
from helper_methods import random_delay

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