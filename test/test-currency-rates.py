import requests
from datetime import datetime

def fetchUSDRates(date):
    return fetchRates('USD', date)


def fetchRates(base, date):
    url = f"https://api.exchangerate.host/{date.strftime('%Y-%m-%d')}?base={base}"
    response = requests.get(url)
    data = response.json()

    return data['rates']


data = fetchUSDRates(datetime.now())
print(data['JPY'])
