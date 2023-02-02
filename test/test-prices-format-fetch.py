import time

import requests
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta
from tinydb import TinyDB, Query
from datetime import datetime

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


def getPrices():
    previousMonth = datetime.now() - relativedelta(months=1)
    lastMonthDays = collectLastMonthDays(2021, 1, previousMonth.year, previousMonth.month)

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
    lastMonthDays = collectLastMonthDays(2021, 1, previousMonth.year, previousMonth.month)

    result = []

    for lastMonthDay in lastMonthDays:

        if lastMonthDay not in hydraUSDRatesDates:
            result.append(lastMonthDay)

    return result

def insertRate(rate, date):
    database = TinyDB('database.json')
    hydraUSDRatesTable = database.table('hydra_usd_prices')
    hydraUSDRatesTable.insert({'rate': float(rate), 'date': date.strftime('%d-%m-%Y')})


print("Initialization: Phase Hydra USD Prices")
print("Note that the process may take time! That is due to the rate limiting from the free CoinGecko API!")

#TODO: Retrieve from the database the last fetched date.

missingLastMonthDays = getMissingLastMonthDays()

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
