import time

import requests
from dateutil.relativedelta import relativedelta
from requests import ReadTimeout
from tinydb import TinyDB, Query
from datetime import datetime
import date_utils
import logging

DATABASE_NAME = "hydrachain-staking-statistics.json"
LAST_DAY_OF_MONTH_PRICES_TABLE_NAME = "hydra_prices_last_day_of_month"
COIN_GECKO_RATE_LIMIT_RETRY_SECONDS = 15
COIN_GECKO_REQUEST_TIMEOUT_SECONDS = 3


class RateLimitException(Exception):
    pass


class GateawayTimeoutException(Exception):
    pass

"""
Fetch and store for faster access the not stored prices of the cryptocurrency hydra for
all month's last days since it exists.
Note that it may take time for the synchronization according to how many last month days
are not yet synchronized.
That is due to the using of the free CoinGecko's API version for retrieving historical
cryptocurrency prices.
"""


def synchronizeAllMonthsPricesForLastMonthDay():
    missingLastMonthDays = _getUnsynchronizedLastDaysOfMonth()

    if missingLastMonthDays:
        logging.info("Synchronization of %s Hydra's USD prices at the end of the month is required.",
                     len(missingLastMonthDays))
        logging.info("It may take some due to rate limiting from CoinGecko's API!")

    for missingLastMonthDay in missingLastMonthDays:

        fetchedSuccessful = False
        while not fetchedSuccessful:
            try:
                price = _fetchHydraUSDPriceAtGivenDate(missingLastMonthDay)
                _saveDatabaseLastDayOfMonthPrice(price, missingLastMonthDay)
                logging.info("Synchronized date %s. Price was %s USD", missingLastMonthDay, price)
                fetchedSuccessful = True
            except RateLimitException:
                logging.debug("Rate limiting from CoinGecko! Waiting %s seconds and retrying again!",
                              COIN_GECKO_RATE_LIMIT_RETRY_SECONDS)
                time.sleep(COIN_GECKO_RATE_LIMIT_RETRY_SECONDS)
            except ReadTimeout:
                logging.debug("502 timeout to CoinGecko. Retrying again!")

    logging.debug("Synchronization of %s Hydra's USD prices finished!", len(missingLastMonthDays))

def getAllLastDayOfMonthPricesFormatted():
    allLastDayOfMonthPrices = _getDatabaseAllLastDayOfMonthPrices()

    lastDayOfMonthPricesFormatted = {}

    for lastDayOfMonthPrice in allLastDayOfMonthPrices:
        date = '{d.month}/{d.year}'.format(d=datetime.strptime(lastDayOfMonthPrice['date'], '%d-%m-%Y'))
        lastDayOfMonthPricesFormatted[date] = float(lastDayOfMonthPrice['price'])

    return lastDayOfMonthPricesFormatted


"""
Fetch the hydra's USD price at a given date using the CoinGecko's API.
Note that there is a limit on the requests per minute. Due to that a RateLimitException will
be thrown if the limit is exceeded.
"""


def _fetchHydraUSDPriceAtGivenDate(date):
    url = f"https://api.coingecko.com/api/v3/coins/hydra/history?date={date.strftime('%d-%m-%Y')}&localization=false"
    logging.debug("Executing request to CoinGecko. URL: %s", url)
    response = requests.get(url, timeout=COIN_GECKO_REQUEST_TIMEOUT_SECONDS)

    if response.status_code == 504:
        logging.debug("Request URL: %s resulted in 504 - gateaway timeout", url)
        raise GateawayTimeoutException()

    if response.status_code == 429:
        logging.debug("Request URL: %s resulted in 429 - too many request", url)
        raise RateLimitException("Due to using the free API of CoinGecko there is a limit of the request per minute.")

    data = response.json()
    logging.debug("Request URL: %s responded with date: %s", url, data)
    return data['market_data']['current_price']['usd']


"""
The synchronized are the ones that are stored in our database.
"""


def _getSynchronizedLastDaysOfMonth():
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_PRICES_TABLE_NAME)
    lastDayOfMonthPrices = table.all()

    lastDayOfMonthPriceDates = []

    for lastDayOfMonthPrice in lastDayOfMonthPrices:
        lastDayOfMonthPriceDate = datetime.strptime(lastDayOfMonthPrice['date'], '%d-%m-%Y').date()

        lastDayOfMonthPriceDates.append(lastDayOfMonthPriceDate)

    return lastDayOfMonthPriceDates


"""
The unsynchronized are the ones not stored in our database.
"""


def _getUnsynchronizedLastDaysOfMonth():
    synchronized = _getSynchronizedLastDaysOfMonth()

    previousMonth = datetime.now() - relativedelta(months=1)
    lastMonthDays = date_utils.getLastMonthDays(2021, 1, previousMonth.year, previousMonth.month)

    unsynchronized = []

    for lastMonthDay in lastMonthDays:

        if lastMonthDay not in synchronized:
            unsynchronized.append(lastMonthDay)

    return unsynchronized


def _saveDatabaseLastDayOfMonthPrice(price, date):
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_PRICES_TABLE_NAME)

    insertionObject = {'price': float(price), 'date': date.strftime('%d-%m-%Y')}
    table.insert(insertionObject)
    logging.debug("Stored in database %s in table %s the record/s: %s", DATABASE_NAME,
                  LAST_DAY_OF_MONTH_PRICES_TABLE_NAME, insertionObject)


def _getDatabaseAllLastDayOfMonthPrices():
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_PRICES_TABLE_NAME)
    lastDayOfMonthPrices = table.all()
    logging.debug("Retrieved from database %s in table %s the record/s: %s", DATABASE_NAME,
                  LAST_DAY_OF_MONTH_PRICES_TABLE_NAME, lastDayOfMonthPrices)
    return lastDayOfMonthPrices


# test
# logging.basicConfig(level=logging.DEBUG)
# synchronizeAllMonthsPricesForLastMonthDay()
