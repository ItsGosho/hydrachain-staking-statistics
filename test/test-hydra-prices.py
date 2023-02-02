import requests
from datetime import datetime


def fetchUSDPrice(date):
    url = f"https://api.coingecko.com/api/v3/coins/hydra/history?date={date.strftime('%d-%m-%Y')}&localization=false"
    response = requests.get(url)
    data = response.json()

    return data['market_data']['current_price']['usd']


data = fetchUSDPrice(datetime.now())
print(data)
