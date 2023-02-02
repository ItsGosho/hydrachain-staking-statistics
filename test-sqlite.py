from tinydb import TinyDB, Query
from datetime import datetime

class CurrencyRates:

    def __init__(self, base, date, rates):
        self.base = base
        self.date = date
        self.rates = rates


db = TinyDB('database.json')
table = db.table('currency_rates')

currencyRates = CurrencyRates('USD', datetime.now(), '')

#table.insert({'value': True})
#table.insert(currencyRates)



