from tinydb import TinyDB, Query


class HydraUSDPrice:
    def __init__(self, price, date):
        self.price = price
        self.date = date


def insertHydraUSDPrice(hydraUSDPrice):
    database = TinyDB('database.json')
    hydraUSDRatesTable = database.table('hydra_usd_prices')
    insertionObject = {'price': float(hydraUSDPrice.price), 'date': hydraUSDPrice.date.strftime('%d-%m-%Y')}
    hydraUSDRatesTable.insert(insertionObject)
