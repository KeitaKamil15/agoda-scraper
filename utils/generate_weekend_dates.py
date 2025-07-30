from datetime import datetime, timedelta

def generate_weekend_dates(start_date: datetime, end_date: datetime):
    current_date = start_date
    weekends = []
    while current_date <= end_date:
        if current_date.weekday() in (5, 6):  # 5 = Sabtu, 6 = Minggu
            weekends.append(current_date)
        current_date += timedelta(days=1)
    return weekends
