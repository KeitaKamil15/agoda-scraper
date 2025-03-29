import time
import random
import json
import os
from playwright.sync_api import sync_playwright
from app.routers.booking_utils.helper_methods import get_dates, random_delay, simulate_human_mouse  # Ensure these functions exist in your helper_methods module
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# Define user-agents specific to each browser
with open('app/routers/booking_utils/user_agents.json') as f:
    USER_AGENTS = json.load(f)

def dismiss_login_popup(page):
    """
    Attempts to close the login/signin popup if it appears.
    Returns True if popup was found and dismissed, False otherwise.
    """
    try:
        # Short timeout to check if popup exists without waiting too long
        dismiss_button = page.wait_for_selector("//button[@aria-label='Dismiss sign-in info.']", timeout=3000)
        if dismiss_button:
            print("Login popup detected. Attempting to dismiss...")
            # Add some random delay before clicking to appear more human-like
            random_delay(0.5, 1.5)
            dismiss_button.click()
            random_delay(1, 2)
            print("Login popup dismissed successfully")
            return True
    except PlaywrightTimeoutError:
        # No popup found, which is fine
        return False
    except Exception as e:
        print(f"Error handling login popup: {e}")
        return False
    return False

def visit_booking_homepage(p):
    """
    Initializes the browser, context, and page. Navigates to the Booking.com homepage 
    with human-like behavior. Returns the tuple (page, context, browser) for further actions.
    """
    # Randomly choose a browser
    browser_name = random.choice(["firefox", "chromium"])
    print(f"Using browser: {browser_name}")
    # Pick a random user agent for the selected browser
    user_agent = random.choice(USER_AGENTS[browser_name])
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
    page.goto("https://www.booking.com", wait_until="networkidle")
    random_delay(1, 3)
    
    # Check for and handle login popup on homepage
    dismiss_login_popup(page)
    
    # Mimic a small scroll to emulate human behavior
    page.evaluate("window.scrollBy(0, window.innerHeight/8)")
    random_delay(1, 2)
    return page, context, browser

def search_booking_homepage(page, city_name: str):
    """
    Performs the homepage search by entering the city name, selecting check-in and check-out dates,
    and clicking the search button.
    """
    # Fill in the search field
    page.type("xpath=//*[@name='ss']", city_name, delay=random.randint(50, 150))
    random_delay(1, 2)
    print(f"Entered city name: {city_name}")
    
    # Open the date selector
    page.click("xpath=//*[@data-testid='searchbox-dates-container']")
    random_delay(1, 2)
    # Pick check-in and check-out dates
    tomorrow_date, day_after_tomorrow_date = get_dates()
    page.click(f"xpath=//span[@data-date='{tomorrow_date}']")
    page.click(f"xpath=//span[@data-date='{day_after_tomorrow_date}']")
    random_delay(1, 2)
    print(f"Selected check-in: {tomorrow_date}, check-out: {day_after_tomorrow_date}")
    
    # Simulate human mouse movement before clicking the search button
    simulate_human_mouse(page)
    page.click("xpath=//*[@id='indexsearch']/div[2]/div/form/div/div[4]/button")
    random_delay(5, 6)
    print("Clicked search button...")

def scroll_and_load_all_results(page):
    """
    Continuously scrolls down the page and clicks 'Load more results' (if visible)
    until there are no more hotels to load.
    """
    load_more_xpath = '//button[span[text()="Load more results"]]'
    
    while True:
        # Check for login popup after each scroll
        dismiss_login_popup(page)
        
        # Scroll down to ensure the button is in view
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        random_delay(2, 4)  # Mimic human pause
        
        try:
            # Wait for the button to appear (short timeout)
            page.wait_for_selector(load_more_xpath, timeout=3000)
        except PlaywrightTimeoutError:
            print("No more 'Load more results' button. Reached the bottom of listings.")
            break
        
        # Click on the 'Load more results' button
        page.click(load_more_xpath)
        print("Clicked 'Load more results' button...")
        random_delay(2, 4)
        
        # Optionally scroll further after clicking
        page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
        random_delay(2, 4)
    
    random_delay(1, 3)

def booking_list_scraping(city_name: str = "", output_file: str = None):
    """
    Orchestrates the Booking.com scraping process. Ensures the output directory exists.
    """
    # If no output file is specified, create a default one
    if output_file is None:
        base_dir = os.path.join(os.path.dirname(__file__), 'html_files')
        os.makedirs(base_dir, exist_ok=True)
        output_file = os.path.join(base_dir, f"{city_name.lower()}_booking.html")
    
    try:
        with sync_playwright() as p:
            # Initialize browser and visit Booking.com homepage
            page, context, browser = visit_booking_homepage(p)
            
            # Perform the search on the homepage
            search_booking_homepage(page, city_name)
            
            # Check for popup after search results load
            dismiss_login_popup(page)
            
            # Wait for search results container to ensure the page is loaded
            page.wait_for_selector('//div[@data-results-container="1"]')
            
            # Check for popup after results page loads
            dismiss_login_popup(page)
            
            # Scroll and click "Load more results" until reaching the bottom
            scroll_and_load_all_results(page)
            
            # Save final HTML to file
            html_content = page.content()
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            print(f"Final page HTML saved to {output_file}")
            
            # Close the context and browser
            context.close()
            browser.close()
    except Exception as e:
        print(f"Failed to simulate booking.com: {e}")    
    
if __name__ == "__main__":
    booking_list_scraping(city_name='dhaka', output_file='dhaka.html')