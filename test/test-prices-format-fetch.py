import time

import requests
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tinydb import TinyDB, Query
from datetime import datetime
import date_utils

class RateLimitException(Exception):
    pass

def fetchHydraUSDPrice(date):
    url = f"https://api.coingecko.com/api/v3/coins/hydra/history?date={date.strftime('%d-%m-%Y')}&localization=false"
    response = requests.get(url)
    data = response.json()

    if response.status_code == 429:
        raise RateLimitException()

    print(data)
    return data['market_data']['current_price']['usd']


def getPrices():
    previousMonth = datetime.now() - relativedelta(months=1)
    lastMonthDays = date_utils.getLastMonthDays(2021, 1, previousMonth.year, previousMonth.month)

    prices = []

    for lastMonthDay in lastMonthDays:
        hydraPriceUSD = fetchHydraUSDPrice(lastMonthDay)
        prices.append({'test': float(hydraPriceUSD)})

    return prices

def getDates():
    database = TinyDB('database.json')
    hydraUSDRatesTable = database.table('hydra_usd_prices')
    hydraUSDRates = hydraUSDRatesTable.all()

    results = []

    for hydraUSDRate in hydraUSDRates:
        hydraUSDRateDate = datetime.strptime(hydraUSDRate['date'], '%d-%m-%Y').date()

        results.append(hydraUSDRateDate)

    return results

"""
Look into the database with the Hydra USD Rates, which last month days are missing and require fetching.
"""
def getMissingLastMonthDays():
    hydraUSDRatesDates = getDates()

    previousMonth = datetime.now() - relativedelta(months=1)
    lastMonthDays = date_utils.getLastMonthDays(2021, 1, previousMonth.year, previousMonth.month)

    result = []

    for lastMonthDay in lastMonthDays:

        if lastMonthDay not in hydraUSDRatesDates:
            result.append(lastMonthDay)

    return result

def insertRate(rate, date):
    database = TinyDB('database.json')
    hydraUSDRatesTable = database.table('hydra_usd_prices')
    hydraUSDRatesTable.insert({'rate': float(rate), 'date': date.strftime('%d-%m-%Y')})


#TODO: Retrieve from the database the last fetched date.

missingLastMonthDays = getMissingLastMonthDays()

if missingLastMonthDays:
    print("Synchronization of the Hydra USD Prices is required.")
    print("It may take some time depending, when you last used the program!")
    print("That is due to rate limiting from CoinGecko's API!")

for missingLastMonthDay in missingLastMonthDays:

    fetchedSuccessful = False
    while not fetchedSuccessful:
        try:
            hydraUSDPrice = fetchHydraUSDPrice(missingLastMonthDay)
            print(missingLastMonthDay)
            insertRate(hydraUSDPrice, missingLastMonthDay)
            fetchedSuccessful = True
        except RateLimitException:
            print("Sleeping for 15 seconds!")
            time.sleep(15)


# asd = getPrices()
# print(asd)
