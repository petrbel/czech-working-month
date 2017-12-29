import argparse
import datetime
from enum import Enum

import pandas as pd

from .utils.date import get_national_holiday, date_range


class DayType(Enum):
    BUSINESS_DAY = 0
    WEEKEND = 1
    HOLIDAY = 2

    def to_string(self) -> str:
        if self == DayType.BUSINESS_DAY:
            return 'Business day'
        elif self == DayType.WEEKEND:
            return 'Weekend'
        elif self == DayType.HOLIDAY:
            return 'National Holiday'
        else:
            raise ValueError('Unknown day type.')


class CzechWorkingMonth:
    def __init__(self, day: int, month: int, year: int, hours_per_day: int=8, part_time_ratio: float=1.0):
        self.day = day
        self.month = month
        self.year = year
        self.hours_per_day = hours_per_day
        self.part_time_ratio = part_time_ratio

        # compute data
        self.data = self._compute_data()

        # regular
        self.business_days = len(self.data[self.data['day_type'] == DayType.BUSINESS_DAY])
        self.business_hours = self.business_days * hours_per_day

        # part-time
        self.business_days_part_time = self.business_days * part_time_ratio
        self.business_hours_part_time = self.business_hours * part_time_ratio

        # regular till now
        self.business_days_passed = len(self.data[self.data['day_type'] == DayType.BUSINESS_DAY][self.data['date'] < datetime.datetime.now().date()])
        self.business_hours_passed = self.business_days_passed * hours_per_day
        self.business_hours_remaining = self.business_hours - self.business_hours_passed

        # part-time till now
        self.business_hours_part_time_passed = self.business_hours_passed * part_time_ratio
        self.business_hours_part_time_remaining = self.business_hours_part_time - self.business_hours_part_time_passed

    def _compute_data(self) -> pd.DataFrame:
        """Compute month statistics."""
        next_month = self.month + 1 if self.month < 12 else 1
        next_year = self.year if self.month < 12 else self.year + 1

        data = pd.DataFrame()

        for day_num, date in enumerate(date_range(datetime.date(self.year, self.month, 1),
                                                  datetime.date(next_year, next_month, 1)),
                                       1):
            is_weekend = date.weekday() > 4
            holiday = get_national_holiday(date)

            if holiday is not None:
                data = data.append({'date': date, 'day_type': DayType.HOLIDAY, 'note': holiday.name_en},
                                   ignore_index=True)
            elif is_weekend:
                data = data.append({'date': date, 'day_type': DayType.WEEKEND,
                                    'note': ('Saturday' if date.weekday() == 5 else 'Sunday')},
                                   ignore_index=True)
            else:
                data = data.append({'date': date, 'day_type': DayType.BUSINESS_DAY, 'note': ''},
                                   ignore_index=True)

        return data


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

    current_day = today.day
    current_month = args.month or today.month
    current_year = args.year or today.year

    cwm = CzechWorkingMonth(current_day, current_month, current_year, 8, 0.6)

    print(cwm.data)
    print('========================')
    print('Full-time')
    print('========================')
    print(f'> Total number of business days: {cwm.business_days}')
    print(f'> Total number of business hours: {cwm.business_hours}')
    print(f'> Number of passed business days (until today, exclusive): {cwm.business_days_passed}')
    print(f'> Number of passed business hours (until today, exclusive): {cwm.business_hours_passed}')
    print(f'> Number of remaining business hours (including today): {cwm.business_hours_remaining}')
    print()
    print('========================')
    print(f'Part-time ({cwm.part_time_ratio}x)')
    print('========================')
    print(f'> Total number of full {cwm.hours_per_day}-hours business days: {cwm.business_days_part_time}')
    print(f'> Total number of business hours: {cwm.business_hours_part_time}')
    print(f'> Number of passed business hours (until today, exclusive): {cwm.business_hours_part_time_passed}')
    print(f'> Number of remaining business hours (including today): {cwm.business_hours_part_time_remaining}')


if __name__ == '__main__':
    pd.set_option("display.max_rows", 40)
    pd.set_option('expand_frame_repr', False)
    main()
