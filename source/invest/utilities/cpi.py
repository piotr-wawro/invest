import csv
from datetime import date
from math import isnan, nan
import math
from pathlib import Path

from invest.utilities.date import fraction_of_month, is_same_month


class CPI:
    def __init__(self, path: str) -> None:
        data = CPI._read_csv(path)
        self.cpi_end = CPI._get_end(data)
        self.cpi_start = CPI._get_start(data)
        self.cpi = CPI._get_cpi(data)

    def _read_csv(path) -> list[list[str]]:
        """Read csv with CPI data. Header row is removed."""

        def str_to_float(str: str) -> float:
            try:
                return float(str)
            except ValueError:
                return nan

        with Path(path).open() as file:
            data = csv.reader(file, delimiter='\t')
            data = list(data)[1:]
        return [[str_to_float(x) for x in row] for row in data]

    def _get_end(data: list[list[str]]) -> date:
        """Find last recorded data of cpi."""
        max_year = max(data)
        max_month = 12 if nan not in max_year else max_year.index(nan) - 1
        return date(int(max_year[0]), max_month, 1)

    def _get_start(data: list[list[str]]) -> date:
        """Find out since when data is collected."""
        min_year = min(data)
        min_month = 1 if nan not in min_year else len(min_year) - min_year[::-1].index(nan)
        return date(int(min_year[0]), min_month, 1)

    def _get_cpi(data: list[list[float]]) -> list[float]:
        """Flatten matrix into list."""
        return [x/100
                for row in sorted(data)
                for x in row[1:]
                if not isnan(x)]

    def _date_to_idx(self, date: date) -> int:
        """Returns index of CPI list corresponding to date."""
        return (date.year-self.cpi_start.year)*12+(date.month-self.cpi_start.month)

    def cumulative_inflation(self, start_date: date|None = None, end_date: date|None = None) -> float:
        """Returns cumulative inflation between two dates."""
        if start_date and start_date < self.cpi_start or end_date and end_date < self.cpi_start:
            raise Exception(f'CPI is recorded since {self.cpi_start}. You try to get data before this date.')
        if start_date and start_date > self.cpi_end or end_date and end_date > self.cpi_end:
            raise Exception(f'CPI is recorded to {self.cpi_end}. You try to get data adter this date.')

        def fraction_of_inflation(start_date: date|None = None, end_date: date|None = None) -> float:
            date = start_date if start_date is not None else end_date
            return fraction_of_month(start_date, end_date)*(self.inflation(date)-1)+1

        if start_date and end_date:
            if is_same_month(start_date, end_date):
                return fraction_of_inflation(start_date, end_date)
            else:
                start_idx = self._date_to_idx(start_date)
                end_idx = self._date_to_idx(end_date)
                cpi_list = self.cpi[start_idx:end_idx+1]

                return fraction_of_inflation(start_date=start_date)*math.prod(cpi_list[1:-1])*fraction_of_inflation(end_date=end_date)
        elif start_date:
            return fraction_of_inflation(start_date=start_date)
        elif end_date:
            return fraction_of_inflation(end_date=end_date)
        else:
            raise Exception("No data provided.")

    def inflation(self, date: date) -> float:
        """Returns inflation in specific month."""
        if date < self.cpi_start:
            raise Exception(f'CPI is recorded since {self.cpi_start}. You try to get data from {date}.')

        return self.cpi[self._date_to_idx(date)]
