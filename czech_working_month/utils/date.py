import datetime
from typing import Optional, Iterable

from czech_holidays import Holiday, Holidays


def date_range(start: datetime.date, end: datetime.date, step=datetime.timedelta(1)) -> Iterable[datetime.date]:
    """Generator providing dates between the start date (inclusive) and the end date (exclusive)."""
    curr = start
    while curr < end:
        yield curr
        curr += step


def get_national_holiday(day: datetime.date) -> Optional[Holiday]:
    """
    For a given date, return the national holiday object if the particular date is a Czech national holiday;
    return None otherwise
    """
    for holiday in Holidays(year=day.year):
        if day == holiday:
            return holiday
    return None
