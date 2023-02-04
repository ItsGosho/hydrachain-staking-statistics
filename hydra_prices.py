import time

import requests
from dateutil.relativedelta import relativedelta
from tinydb import TinyDB, Query
from datetime import datetime
import date_utils

DATABASE_NAME = "hydrachain-staking-statistics.db"
LAST_DAY_OF_MONTH_PRICES_TABLE_NAME = "hydra_prices_last_day_of_month"


class RateLimitException(Exception):
    pass


"""
Fetch and store for faster access the not stored prices of the cryptocurrency hydra for
all month's last days since it exists and return all of them.
Note that it may take time for the synchronization according to how many last month days
are not yet synchronized.
That is due to the using of the free CoinGecko's API version for retrieving historical
cryptocurrency prices.
"""


def synchronizeAllMonthsPricesForLastMonthDay():
    missingLastMonthDays = getUnsynchronizedLastDaysOfMonth()

    if missingLastMonthDays:
        print("Synchronization of the Hydra USD Prices is required.")
        print("It may take some time depending, when you last used the program!")
        print("That is due to rate limiting from CoinGecko's API!")

    for missingLastMonthDay in missingLastMonthDays:

        fetchedSuccessful = False
        while not fetchedSuccessful:
            try:
                price = fetchHydraUSDPriceAtGivenDate(missingLastMonthDay)
                saveDatabaseLastDayOfMonthPrice(price, missingLastMonthDay)
                print("Synchronize date {}".format(missingLastMonthDay))
                fetchedSuccessful = True
                time.sleep(1) # It is not good idea to create a burst volume of request to CoinGecko's API
            except RateLimitException:
                print("Sleeping for 15 seconds!")
                time.sleep(15)

    hydraUSDPrices = getDatabaseAllLastDayOfMonthPrices()

    # Format result

    result = {}

    for hydraUSDPrice in hydraUSDPrices:
        date = '{d.month}/{d.year}'.format(d=datetime.strptime(hydraUSDPrice['date'], '%d-%m-%Y'))
        result[date] = float(hydraUSDPrice['price'])

    print(result)


"""
Fetch the hydra's USD price at a given date using the CoinGecko's API.
Note that there is a limit on the requests per minute. Due to that a RateLimitException will
be thrown if the limit is exceeded.
"""


def fetchHydraUSDPriceAtGivenDate(date):
    url = f"https://api.coingecko.com/api/v3/coins/hydra/history?date={date.strftime('%d-%m-%Y')}&localization=false"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 429:
        raise RateLimitException()

    return data['market_data']['current_price']['usd']


"""
The synchronized are the ones that are stored in our database.
"""


def getSynchronizedLastDaysOfMonth():
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


def getUnsynchronizedLastDaysOfMonth():
    synchronized = getSynchronizedLastDaysOfMonth()

    previousMonth = datetime.now() - relativedelta(months=1)
    lastMonthDays = date_utils.getLastMonthDays(2021, 1, previousMonth.year, previousMonth.month)

    unsynchronized = []

    for lastMonthDay in lastMonthDays:

        if lastMonthDay not in synchronized:
            unsynchronized.append(lastMonthDay)

    return unsynchronized

def saveDatabaseLastDayOfMonthPrice(price, date):
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_PRICES_TABLE_NAME)

    insertionObject = {'price': float(price), 'date': date.strftime('%d-%m-%Y')}
    table.insert(insertionObject)

def getDatabaseAllLastDayOfMonthPrices():
    database = TinyDB(DATABASE_NAME)
    table = database.table(LAST_DAY_OF_MONTH_PRICES_TABLE_NAME)
    return table.all()

#test

synchronizeAllMonthsPricesForLastMonthDay()