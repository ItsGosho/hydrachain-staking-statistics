from tinydb import TinyDB, Query
from datetime import datetime

class CurrencyRates:

    def __init__(self, base, date, rates):
        self.base = base
        self.date = date
        self.rates = rates


database = TinyDB('database.json')
hydraUSDRatesTable = database.table('hydra_usd_rates')

#hydraUSDRatesTable.insert({'rate': float(2.50), 'date': datetime.now().date().strftime('%d-%m-%Y')})

testQuery = Query()
result = hydraUSDRatesTable.search(testQuery.date =='01-02-2023')
print(result)

