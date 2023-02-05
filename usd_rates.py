import time

import requests
from dateutil.relativedelta import relativedelta
from requests import ReadTimeout
from tinydb import TinyDB, Query
from datetime import datetime
import date_utils
import logging

DATABASE_NAME = "hydrachain-staking-statistics.json"
LAST_DAY_OF_MONTH_USD_RATES_TABLE_NAME = "last_day_of_month_usd_rates"


def synchronizeAllMonthsPricesForLastMonthDay():
    missingLastMonthDays = _getUnsynchronizedLastDaysOfMonth()

    if missingLastMonthDays:
        logging.info("Synchronization of %s USD rates at the end of the month is required.",
                     len(missingLastMonthDays))

    for missingLastMonthDay in missingLastMonthDays:

        fetchedSuccessful = False
        while not fetchedSuccessful:
            price = _fetchUSDRates(missingLastMonthDay)
            _saveDatabaseLastDayOfMonthPrice(price, missingLastMonthDay)
            logging.info("Synchronized date %s. USD Rates.", missingLastMonthDay)
            fetchedSuccessful = True

    logging.debug("Synchronization of USD prices finished!")


def getAllLastDayOfMonthPricesFormatted():
    allLastDayOfMonthPrices = _getDatabaseAllLastDayOfMonthPrices()

    lastDayOfMonthPricesFormatted = {}

    for lastDayOfMonthPrice in allLastDayOfMonthPrices:
        date = '{d.month}/{d.year}'.format(d=datetime.strptime(lastDayOfMonthPrice['date'], '%d-%m-%Y'))
        lastDayOfMonthPricesFormatted[date] = lastDayOfMonthPrice['rates']

    return lastDayOfMonthPricesFormatted


def fetchCurrentUSDRates():
    return _fetchRates('USD', datetime.now())


def _fetchUSDRates(date):
    return _fetchRates('USD', date)


def _fetchRates(base, date):
    url = f"https://api.exchangerate.host/{date.strftime('%Y-%m-%d')}?base={base}"
    response = requests.get(url)
    data = response.json()

    return data['rates']


def _getSynchronizedLastDaysOfMonth():
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_USD_RATES_TABLE_NAME)
    lastDayOfMonthPrices = table.all()

    lastDayOfMonthPriceDates = []

    for lastDayOfMonthPrice in lastDayOfMonthPrices:
        lastDayOfMonthPriceDate = datetime.strptime(lastDayOfMonthPrice['date'], '%d-%m-%Y').date()

        lastDayOfMonthPriceDates.append(lastDayOfMonthPriceDate)

    return lastDayOfMonthPriceDates


def _getUnsynchronizedLastDaysOfMonth():
    synchronized = _getSynchronizedLastDaysOfMonth()

    previousMonth = datetime.now() - relativedelta(months=1)
    lastMonthDays = date_utils.getLastMonthDays(2021, 1, previousMonth.year, previousMonth.month)

    unsynchronized = []

    for lastMonthDay in lastMonthDays:

        if lastMonthDay not in synchronized:
            unsynchronized.append(lastMonthDay)

    return unsynchronized


def _saveDatabaseLastDayOfMonthPrice(prices, date):
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_USD_RATES_TABLE_NAME)

    insertionObject = {'rates': prices, 'date': date.strftime('%d-%m-%Y')}
    table.insert(insertionObject)
    logging.debug("Stored in database %s in table %s the record/s: %s", DATABASE_NAME,
                  LAST_DAY_OF_MONTH_USD_RATES_TABLE_NAME, insertionObject)


def _getDatabaseAllLastDayOfMonthPrices():
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_USD_RATES_TABLE_NAME)
    lastDayOfMonthPrices = table.all()
    logging.debug("Retrieved from database %s in table %s the record/s: %s", DATABASE_NAME,
                  LAST_DAY_OF_MONTH_USD_RATES_TABLE_NAME, lastDayOfMonthPrices)
    return lastDayOfMonthPrices