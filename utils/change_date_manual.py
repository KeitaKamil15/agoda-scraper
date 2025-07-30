from .helper_methods import get_dates, random_delay, different_dates
from datetime import datetime, timedelta

def change_date_manual(page, target_date: datetime):
    print("="*100)
    page.locator("#check-in-box").first.click()
    page.wait_for_timeout(500)  # opsional, 0.5 detik

    date = page.locator('div.DayPicker-Caption.DayPicker-Caption-Wide').first
    date.wait_for(state='visible', timeout=5000)
    date_now = date.text_content()

    target_month_year = target_date.strftime("%Y-%m-01")  # Awal bulan dari target_date
    date_now_formatted, target_month_formatted, date_gap = different_dates(date_now, target_month_year)

    page.wait_for_timeout(1000)

    for i in range(date_gap):
        print(f"arrow button {i}")

        locator = page.locator('button[data-selenium="calendar-next-month-button"]').first
        locator.wait_for(state='visible', timeout=30000)

        if locator.is_enabled():
            locator.click()
            page.wait_for_timeout(1000)
        else:
            print("Tombol next bulan disable, break loop")
            break

    # Pilih tanggal spesifik (bukan hanya bulan)
    target_day = target_date.strftime("%Y-%m-%d")
    page.click(f"xpath=//span[@data-selenium-date='{target_day}']")

    page.locator("button", has_text='Update').click()
    random_delay(0.5, 1)
    print(f"Clicked update button for date {target_day}")
    print("="*100)

    page.evaluate("window.scrollBy(0, window.innerHeight/8)")
    random_delay(1, 2)
