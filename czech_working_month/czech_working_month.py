from czech_holidays import Holiday, Holidays
from tabulate import tabulate

import argparse
import datetime
import math
from typing import Optional, Iterable


def _date_range(start: datetime.date, end: datetime.date, step=datetime.timedelta(1)) -> Iterable[datetime.date]:
    """Generator providing dates between the start date (inclusive) and the end date (exclusive)."""
    curr = start
    while curr < end:
        yield curr
        curr += step


def _get_national_holiday(day: datetime.date) -> Optional[Holiday]:
    """
    For a given date, return the national holiday object if the particular date is a Czech national holiday;
    return None otherwise
    """
    for holiday in Holidays(year=day.year):
        if day == holiday:
            return holiday
    return None


def show_working_month(month: int, year: int, hours_per_day: int, part_time_ratio: float) -> None:
    """Show overall month statistics."""
    next_month = month + 1 if month < 12 else 1
    next_year = year if month < 12 else year + 1

    total_working_days = 0
    message = []
    for day in _date_range(datetime.date(year, month, 1), datetime.date(next_year, next_month, 1)):
        is_weekend = day.weekday() > 4
        holiday = _get_national_holiday(day)

        day_type = 'working day'
        if holiday is not None:
            day_type = 'National holiday: {}'.format(holiday.name_en)
        elif is_weekend:
            day_type = 'weekend'
        message.append([day, day_type])

        if is_weekend or holiday is not None:
            continue

        total_working_days += 1

    print(tabulate(message, headers=['date', 'day type']))
    print()
    print('----------------------')
    print('Total working days: {}'.format(total_working_days))
    print('Full-time working hours: {}'.format(total_working_days * hours_per_day))

    if not math.isclose(part_time_ratio, 1.0, abs_tol=0.001):
        part_time_hours = int(total_working_days * hours_per_day * part_time_ratio)
        print('{}-time working hours: {} (i.e. ~{:.2f} {}-hours days)'.format(part_time_ratio,
                                                                         part_time_hours,
                                                                         part_time_hours/hours_per_day,
                                                                         hours_per_day))


def main():
    parser = argparse.ArgumentParser('Working month')
    parser.add_argument('month', nargs='?', type=int, default=None, help='month')
    parser.add_argument('year', nargs='?', type=int, default=None, help='year')
    parser.add_argument('-d', '--day-length', type=int, default=8,
                        help='number of working hours per regular working day')
    parser.add_argument('-p', '--part-time-ratio', type=float, default=1.0,
                        help='part-time fraction of the full-time')
    args = parser.parse_args()

    today = datetime.date.today()

    current_month = args.month or today.month
    current_year = args.year or today.year

    show_working_month(month=current_month,
                       year=current_year,
                       hours_per_day=args.day_length,
                       part_time_ratio=args.part_time_ratio)

if __name__ == '__main__':
    main()
