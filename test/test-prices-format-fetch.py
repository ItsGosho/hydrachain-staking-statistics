import requests
import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta


def fetchHydraUSDPrice(date):
    url = f"https://api.coingecko.com/api/v3/coins/hydra/history?date={date.strftime('%d-%m-%Y')}&localization=false"
    response = requests.get(url)
    data = response.json()

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

asd = getPrices()
print(asd)
