from helper_methods import get_dates, random_delay
from datetime import datetime, timedelta

def change_date_book(page):
    print("="*100)
    page.locator('span.RoomGrid-searchTimeOutAction').first.click()
    
    check_in_date, check_out_date = get_dates()
    print(f"Date sebelum di ubah {check_in_date}, {check_out_date}")

    # Ubah ke objek datetime satu per satu
    check_in_date_dt = datetime.strptime(check_in_date, "%Y-%m-%d")
    check_out_date_dt = datetime.strptime(check_out_date, "%Y-%m-%d")

    # Tambah hari sesuai kebutuhan
    check_in_date_dt = check_in_date_dt + timedelta(days=1)
    check_out_date_dt = check_out_date_dt + timedelta(days=2)

    # Kembalikan ke string lagi
    check_in_date = check_in_date_dt.strftime("%Y-%m-%d")
    check_out_date = check_out_date_dt.strftime("%Y-%m-%d")

    print(f"Date sesudah di ubah {check_in_date}")
    print(f"Date sesudah di ubah {check_out_date}")

    # Click on the check-in date
    page.click(f"xpath=//span[@data-selenium-date='{check_in_date}']")
    random_delay(1, 2)
    print(f"Selected check-in date: {check_in_date}")

    page.click(f"xpath=//span[@data-selenium-date='{check_out_date}']")
    random_delay(1, 2)
    print(f"Selected check-out date: {check_out_date}")

    page.locator("button", has_text='Update').click()
    random_delay(0.5, 1)
    print("Clicked update button...")
    print("="*100)

    # Mimic a small scroll to emulate human behavior
    page.evaluate("window.scrollBy(0, window.innerHeight/8)")
    random_delay(1, 2)

    # return page