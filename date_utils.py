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

def isMonthAndYearEqual(datetime1, datetime2):
    return datetime1.year == datetime2.year and datetime1.month == datetime2.month

class YearMonth:
    def __init__(self, year, month):
        self.year = year
        self.month = month

    """
    Returns the number of days in the month
    """
    def getMonthDays(self):
        return calendar.monthrange(self.year, self.month)[1]

    """
    Returns the number of days that have passed from the month.
    """
    def getPassedDays(self):

        if(self.isTodayMonthAndYear()):
            currentDateTime = datetime.now()
            return currentDateTime.day

        return self.getMonthDays()

    def isTodayMonthAndYear(self):
        currentDateTime = datetime.now()

        return currentDateTime == self

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.year == other.year and self.month == other.month
        if isinstance(other, datetime):
            return self.year == other.year and self.month == other.month
        return False

    def __hash__(self):
        return hash((self.year, self.month))

    def __repr__(self):
        return f'YearMonth({self.year}, {self.month})'
