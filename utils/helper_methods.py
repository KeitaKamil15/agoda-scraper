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


def different_dates(current_month_year,target_month_year):

    # Pemetaan nama bulan Indonesia ke angka bulan
    bulan_mapping = {
    "January": 1,
    "February": 2,
    "March": 3,
    "April": 4,
    "May": 5,
    "June": 6,
    "July": 7,
    "August": 8,
    "September": 9,
    "October": 10,
    "November": 11,
    "December": 12
    }

    # Contoh input
    # current_month_year = "Juli 2025"
    # target_month_year = "September 2025"

     # Pecah teks bulan dan tahun dari string "Month YYYY"
    bulan_skrg, tahun_skrg = current_month_year.strip().split()

    # Pecah target ke dalam YYYY-MM-DD
    tahun_target, bulan_target_num, _ = target_month_year.strip().split("-")

    # Format ulang current_month_year menjadi format "YYYY-MM-01"
    bulan_skrg_num = bulan_mapping[bulan_skrg]
    date_now_formatted = f"{tahun_skrg}-{bulan_skrg_num:02d}-01"

    # Hitung selisih bulan
    selisih_bulan = (
        (int(tahun_target) - int(tahun_skrg)) * 12 +
        (int(bulan_target_num) - bulan_skrg_num)
    )

    return date_now_formatted, target_month_year, selisih_bulan