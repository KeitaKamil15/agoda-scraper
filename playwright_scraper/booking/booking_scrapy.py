import os
import json
import random
import time
from typing import Dict, Optional

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy_playwright.page import PageMethod

# Important: We need to set the reactor before importing other components
# This must happen before any other Twisted or Scrapy imports
import asyncio
from scrapy.utils.reactor import install_reactor
install_reactor('twisted.internet.asyncioreactor.AsyncioSelectorReactor')

# Load user agents
with open('user_agents.json') as f:
    USER_AGENTS = json.load(f)

class BookingSpider(scrapy.Spider):
    name = 'booking_spider'
    
    def __init__(self, city_name: str = "dhaka", output_file: Optional[str] = None, *args, **kwargs):
        super(BookingSpider, self).__init__(*args, **kwargs)
        self.city_name = city_name
        
        # If no output file is specified, create a default one
        if output_file is None:
            base_dir = os.path.join(os.path.dirname(__file__), 'html_files')
            os.makedirs(base_dir, exist_ok=True)
            self.output_file = os.path.join(base_dir, f"{city_name.lower()}_booking.html")
        else:
            self.output_file = output_file
            
        # Import helper methods
        from helper_methods import get_dates, random_delay, simulate_human_mouse
        self.get_dates = get_dates
        self.helper_random_delay = random_delay
        # self.helper_simulate_human_mouse = simulate_human_mouse
    
    async def helper_simulate_human_mouse(self, page):
        """Simulate random human-like mouse movements."""
        width, height = page.viewport_size['width'], page.viewport_size['height']
        
        for _ in range(random.randint(3, 4)):
            # Perform random moves
            x, y = random.randint(0, width), random.randint(0, height)
            await page.mouse.move(x, y, steps=random.randint(5, 10))
            
            # Random pauses - use asyncio.sleep instead of time.sleep
            await asyncio.sleep(random.uniform(0.2, 0.8))
    def random_delay(self, min_time: float = 1.0, max_time: float = 3.0):
        """Add random delay to mimic human behavior"""
        self.helper_random_delay(min_time, max_time)
    
    def start_requests(self):
        # Randomly choose a browser
        browser_name = random.choice(["firefox", "chromium"])
        self.logger.info(f"Using browser: {browser_name}")
        
        # Pick a random user agent for the selected browser
        user_agent = random.choice(USER_AGENTS[browser_name])
        self.logger.info(f"Using user agent: {user_agent}")
        
        # Configure browser launch options
        browser_kwargs = {
            "headless": False
        }
        
        # Configure context options
        context_kwargs = {
            "user_agent": user_agent,
            "viewport": {'width': 1280, 'height': 800},
            "locale": 'en-US'
        }
        
        # Configure page methods to execute on page load
        page_methods = [
            PageMethod("add_init_script", script="Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"),
            PageMethod("wait_for_load_state", state="networkidle")
        ]
        
        # Start with the Booking.com homepage
        yield scrapy.Request(
            url="https://www.booking.com",
            meta={
                "playwright": True,
                "playwright_include_page": True,
                "playwright_page_methods": page_methods,
                "playwright_context_kwargs": context_kwargs,
                "playwright_browser_kwargs": browser_kwargs,
                "playwright_browser": browser_name,
            },
            callback=self.on_homepage
        )
    
    async def dismiss_login_popup(self, page):
        """
        Attempts to close the login/signin popup if it appears.
        Returns True if popup was found and dismissed, False otherwise.
        """
        try:
            # Short timeout to check if popup exists without waiting too long
            dismiss_button = await page.wait_for_selector("//button[@aria-label='Dismiss sign-in info.']", timeout=3000)
            if dismiss_button:
                self.logger.info("Login popup detected. Attempting to dismiss...")
                # Add some random delay before clicking to appear more human-like
                self.random_delay(0.5, 1.5)
                await dismiss_button.click()
                self.random_delay(1, 2)
                self.logger.info("Login popup dismissed successfully")
                return True
        except Exception as e:
            # No popup found or other error, which is fine
            self.logger.debug(f"No login popup or error: {e}")
            return False
        return False
    
    async def on_homepage(self, response):
        """Handle the Booking.com homepage"""
        page = response.meta["playwright_page"]
        
        # Check for and handle login popup on homepage
        await self.dismiss_login_popup(page)
        
        # Mimic a small scroll to emulate human behavior
        await page.evaluate("window.scrollBy(0, window.innerHeight/8)")
        self.random_delay(1, 2)
        
        # Fill in the search field
        await page.type("xpath=//*[@name='ss']", self.city_name, delay=random.randint(50, 150))
        self.random_delay(1, 2)
        self.logger.info(f"Entered city name: {self.city_name}")
        
        # Open the date selector
        await page.click("xpath=//*[@data-testid='searchbox-dates-container']")
        self.random_delay(1, 2)
        
        # Pick check-in and check-out dates
        tomorrow_date, day_after_tomorrow_date = self.get_dates()
        await page.click(f"xpath=//span[@data-date='{tomorrow_date}']")
        await page.click(f"xpath=//span[@data-date='{day_after_tomorrow_date}']")
        self.random_delay(1, 2)
        self.logger.info(f"Selected check-in: {tomorrow_date}, check-out: {day_after_tomorrow_date}")
        
        # Simulate human mouse movement before clicking the search button
        # Using the helper method imported from the original implementation
        await self.helper_simulate_human_mouse(page)
        await page.click("xpath=//*[@id='indexsearch']/div[2]/div/form/div/div[4]/button")
        self.random_delay(5, 6)
        self.logger.info("Clicked search button...")
        
        # Wait for search results container to ensure the page is loaded
        await page.wait_for_selector('//div[@data-results-container="1"]')
        
        # Check for popup after search results load
        await self.dismiss_login_popup(page)
        
        # Process the search results page directly
        await self.parse_search_results(response, page)
    
    async def parse_search_results(self, response, page=None):
        """Parse the search results page and load all results"""
        if page is None:
            page = response.meta["playwright_page"]
        
        # Continuously load more results until we reach the end
        load_more_xpath = '//button[span[text()="Load more results"]]'
        
        while True:
            # Check for login popup after each scroll
            await self.dismiss_login_popup(page)
            
            # Scroll down to ensure the button is in view
            await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
            self.random_delay(2, 4)  # Mimic human pause
            
            try:
                # Wait for the button to appear (short timeout)
                load_more_button = await page.wait_for_selector(load_more_xpath, timeout=3000)
                
                # Click on the 'Load more results' button
                await load_more_button.click()
                self.logger.info("Clicked 'Load more results' button...")
                self.random_delay(2, 4)
                
                # Optionally scroll further after clicking
                await page.evaluate("window.scrollBy(0, document.body.scrollHeight)")
                self.random_delay(2, 4)
                
            except Exception:
                self.logger.info("No more 'Load more results' button. Reached the bottom of listings.")
                break
        
        # Save the final HTML to file
        html_content = await page.content()
        with open(self.output_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        self.logger.info(f"Final page HTML saved to {self.output_file}")

def run_spider(city_name: str = "dhaka", output_file: Optional[str] = None):
    """Run the spider with the given parameters"""
    process = CrawlerProcess({
        'LOG_LEVEL': 'INFO',
        'DOWNLOAD_HANDLERS': {
            "http": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
            "https": "scrapy_playwright.handler.ScrapyPlaywrightDownloadHandler",
        },
        # This must match the reactor set at the top of the file
        'TWISTED_REACTOR': 'twisted.internet.asyncioreactor.AsyncioSelectorReactor',
        'PLAYWRIGHT_LAUNCH_OPTIONS': {
            'headless': False,
        },
        'REQUEST_FINGERPRINTER_IMPLEMENTATION': '2.7',
    })
    
    process.crawl(BookingSpider, city_name=city_name, output_file=output_file)
    process.start()

if __name__ == "__main__":
    run_spider(city_name='dhaka', output_file='dhaka.html')