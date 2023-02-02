import calendar
from datetime import datetime


"""
Collect the last day of each month between two months in a given year

Example:

Arguments:
Between 11/2022 and 02/2023

Result:
[datetime.date(2022, 11, 30), datetime.date(2022, 12, 31), datetime.date(2023, 1, 31), datetime.date(2023, 2, 28)]

If the from year is bigger than the to year, then a empty array will be returned.
"""
def getLastMonthDays(fromYear, fromMonth, toYear, toMonth):
    lastMonthDays = []

    while True:
        if fromYear > toYear:
            return lastMonthDays

        if fromYear == toYear and fromMonth > toMonth:
            return lastMonthDays

        tuple = calendar.monthrange(fromYear, fromMonth)
        date = datetime(fromYear, fromMonth, tuple[1]).date()
        lastMonthDays.append(date)

        fromMonth += 1

        if fromMonth == 13:
            fromMonth = 1
            fromYear += 1