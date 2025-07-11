
from utils.helper_methods import random_delay

def visit_hotel_detail(p, link, USER_AGENTS: dict):
    """
    Navigate to the hotel detail and info page with human-like
    behavior. Returns the tuple (page, context, browser) for 
    further actions.
    """

    print("Doing Visit Hotel Detail")

    # browser_name = random.choice(["firefox"])
    browser_name = "firefox"
    user_agent = USER_AGENTS[browser_name][0]

    # Launch the chosen browser
    browser = getattr(p, browser_name).launch(headless=False)

    context = browser.new_context(
        user_agent=user_agent,
        viewport={'width': 1280, 'height': 800},
        locale='en-US'
    )

    #  Disable WbDriver flag to bypass bot detection
    context.add_init_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

    # Open a new page in the context
    page = context.new_page()

    # navigate to the hotel page
    # page.goto(link, timeout=60000, wait_until="domcontentloaded")
    page.goto(link, timeout=60000, wait_until="load")

    random_delay(1,3)

    #  Mimic a small scroll to emulate human behavior
    page.evaluate("window.scrollBy(0, window.innerHeight/8)")
    random_delay(1,2)

    return page, context, browser