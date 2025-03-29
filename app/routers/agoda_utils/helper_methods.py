from datetime import datetime, timedelta
import random
import time

def random_delay(min_sec=2, max_sec=4):
    """Sleep for a random duration between min_sec and max_sec."""
    time.sleep(random.uniform(min_sec, max_sec))

def simulate_human_mouse(page):
    """Simulate random human-like mouse movements."""
    width, height = page.viewport_size['width'], page.viewport_size['height']
    for _ in range(random.randint(3, 4)):  # Perform random moves
        x, y = random.randint(0, width), random.randint(0, height)
        page.mouse.move(x, y, steps=random.randint(5, 10))
        time.sleep(random.uniform(0.2, 0.8))  # Random pauses


def get_dates():
    """
    Returns tomorrow and day after tomorrow's date in 'YYYY-MM-DD' format.

    Returns:
        tuple: A tuple containing two strings representing tomorrow's date and day after tomorrow's date.
    """
    # Get today's date
    today = datetime.now()

    # Get tomorrow's date
    tomorrow = today + timedelta(days=1)
    tomorrow_date = tomorrow.strftime('%Y-%m-%d')

    # Get day after tomorrow's date
    day_after_tomorrow = today + timedelta(days=2)
    day_after_tomorrow_date = day_after_tomorrow.strftime('%Y-%m-%d')

    return tomorrow_date, day_after_tomorrow_date
