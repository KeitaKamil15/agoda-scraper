import random
from utils.helper_methods import random_delay

def visit_agoda_homepage(p, USER_AGENTS: dict):
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
    # page.goto("https://www.agoda.com/", wait_until="networkidle")
    page.goto("https://www.agoda.com/", wait_until="load")
    random_delay(1, 3)
    # Mimic a small scroll to emulate human behavior
    page.evaluate("window.scrollBy(0, window.innerHeight/8)")
    random_delay(1, 2)
    return page, context, browser