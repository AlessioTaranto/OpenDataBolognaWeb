from datetime import datetime, timedelta

def get_week_range(date: datetime) -> tuple:
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week.date(), end_of_week.date()