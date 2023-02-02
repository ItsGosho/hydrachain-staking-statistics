import requests

def fetchUSDRates():
    url = 'https://api.exchangerate.host/2020-04-04?base=USD'
    response = requests.get(url)
    data = response.json()

    return data['rates']


data = fetchUSDRates()
print(data['JPY'])
