from utils.helper_methods import get_dates, random_delay
from datetime import datetime, timedelta
from utils.helper_methods import different_dates
def change_date_manual(page):
    print("="*100)
    page.locator("#check-in-box").first.click()
    page.wait_for_timeout(500)  # opsional, 0.5 detik

    date = page.locator('div.DayPicker-Caption.DayPicker-Caption-Wide').first
    date.wait_for(state='visible', timeout=5000)
    date_now = date.text_content()

    target_month_year = "2025-09-01"
    date_now_formatted, target_month_formatted, date_gap = different_dates(date_now, target_month_year)

    page.wait_for_timeout(5000)

    for i in range(date_gap):
        print(f"arrow button {i}")

        locator = page.locator('button[data-selenium="calendar-next-month-button"]').first
        # data-selenium="calendar-next-month-button"2
        locator.wait_for(state='visible', timeout=30000)

        if locator.is_enabled():
            locator.click()
            # Tunggu sedikit atau tunggu caption berubah supaya halaman siap
            page.wait_for_timeout(1000)  
            # Atau lebih baik tunggu caption bulan berganti:
            # page.wait_for_function("() => document.querySelector('div.DayPicker-Caption-DayPicker-Caption-Wide').textContent.includes('ExpectedMonth')")
        else:
            print("Tombol next bulan disable, break loop")
            break

    
    # Click on the check-in date
    page.click(f"xpath=//span[@data-selenium-date='{target_month_formatted}']")

    page.locator("button", has_text='Update').click()
    random_delay(0.5, 1)
    print("Clicked update button...")
    print("="*100)

    # Mimic a small scroll to emulate human behavior
    page.evaluate("window.scrollBy(0, window.innerHeight/8)")
    random_delay(1, 2)
