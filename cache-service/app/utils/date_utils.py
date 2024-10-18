from datetime import datetime, timedelta

def get_week_range(date: datetime) -> tuple:
    """
    Returns a tuple containing the start and end dates of the week that the given date falls in.

    The start date will be the Monday of the week, and the end date will be the following Sunday.

    :param date: The date to find the week range for.
    :return: A tuple of two datetime objects: the start and end dates of the week.
    """
    start_of_week = date - timedelta(days=date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    return start_of_week, end_of_week