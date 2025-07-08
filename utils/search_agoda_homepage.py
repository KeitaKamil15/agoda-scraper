from helper_methods import get_dates, random_delay, simulate_human_mouse
import random

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