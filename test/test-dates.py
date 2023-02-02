import calendar
from datetime import datetime

# class LastMonthDay:
#     def __init__(self, year, month, day):
#         self.year = year
#         self.month

"""
Collect the last day of each month between two months in a given year
Example:
From year 2022 and month 11 (November) to year 2023 and month 2 (February)
Result:
[datetime.date(2022, 11, 30), datetime.date(2022, 12, 31), datetime.date(2023, 1, 31), datetime.date(2023, 2, 28)]
"""
def collectLastMonthDays(fromYear, fromMonth, toYear, toMonth):
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


currentDateTime = datetime.now()

lastMonthDays = collectLastMonthDays(2022, 11, 2023, 2)

print(lastMonthDays)
