from calendar import monthrange
from datetime import date

class Flag:
    SAVE = 1<<0
    INV = 1<<1
    SKIP = 1<<2

def months_between(date1: date, date2: date):
    return (date2.year-date1.year)*12+(date2.month-date1.month)

def is_same_month(start_date: date, end_date: date) -> bool:
    return start_date.year == end_date.year and start_date.month == end_date.month

def fraction_of_month(start_date: date|None = None, end_date: date|None = None) -> float:
    if start_date and end_date and start_date > end_date:
        raise Exception("start_date greater than end_date.")

    if start_date and end_date:
        if is_same_month(start_date, end_date):
            month_days = monthrange(start_date.year, start_date.month)[1]
            days = (end_date-start_date).days
            return days/month_days
        else:
            raise Exception("Fraction of month can be calculated only for the same month.")
    elif start_date:
        month_days = monthrange(start_date.year, start_date.month)[1]
        days_to_month_end = month_days - start_date.day + 1
        return days_to_month_end/month_days
    elif end_date:
        month_days = monthrange(end_date.year, end_date.month)[1]
        days_since_month_start = end_date.day - 1
        return days_since_month_start/month_days
    else:
        raise Exception("No data provided.")

def last_day_of_months(start_date: date, end_date: date) -> list[date]:
    if start_date > end_date:
        raise Exception("start_date greater than end_date.")

    tmp_date = date(start_date.year, start_date.month, monthrange(start_date.year, start_date.month)[1])
    dates = [tmp_date]

    while not is_same_month(tmp_date, end_date):
        new_year = tmp_date.year+(tmp_date.month)//12
        new_month = (tmp_date.month)%12+1
        new_day = monthrange(new_year, new_month)[1]
        tmp_date = date(new_year, new_month, new_day)
        dates.append(tmp_date)

    return dates

def first_day_of_months(start_date: date, end_date: date) -> list[date]:
    if start_date > end_date:
        raise Exception("start_date greater than end_date.")

    tmp_date = date(start_date.year, start_date.month, 1)

    if start_date.day == 1:
        dates = [tmp_date]
    else:
        dates = []

    while not is_same_month(tmp_date, end_date):
        new_year = tmp_date.year+(tmp_date.month)//12
        new_month = (tmp_date.month)%12+1
        tmp_date = date(new_year, new_month, 1)
        dates.append(tmp_date)

    return dates
