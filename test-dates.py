import calendar
from datetime import datetime

"""
Collect the last day of each month between two months in a given year
Example:
From year 2022 and month 11 (November) to year 2023 and month 2 (February)
Result:
[31, TODO:]
"""


def collectLastMonthDays(fromYear, fromMonth, toYear, toMonth):
    lastMonthDays = []

    while True:
        if fromYear > toYear:
            return lastMonthDays

        if fromYear == toYear and fromMonth > toMonth:
            return lastMonthDays

        tuple = calendar.monthrange(fromYear, fromMonth)
        lastMonthDays.append(tuple[1])

        fromMonth += 1

        if fromMonth == 13:
            fromMonth = 1
            fromYear += 1


currentDateTime = datetime.now()

lastMonthDays = collectLastMonthDays(2022, 11, 2023, 2)

print(lastMonthDays)
