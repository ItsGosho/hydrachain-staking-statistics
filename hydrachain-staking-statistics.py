import re
import json
import hydra_transactions_reader
import hydra_prices

transactions = hydra_transactions_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
usdToBGNRate = float(1.80) #TODO:
hydraPriceTodayUSD = hydra_prices.getCurrentHydraPrice()
hydra_prices.synchronizeAllMonthsPricesForLastMonthDay()
prices = hydra_prices.getAllLastDayOfMonthPricesFormatted()

byMonth = {}

for transaction in transactions:

    if transaction.type != "Mined":
        continue

    minedMonthYear = str(transaction.date.month) + '/' + str(transaction.date.year)
    minedAmount = float(transaction.amount)

    if minedMonthYear not in byMonth:
        obj = {"total": minedAmount, "transactions": int(1), "blockMin": minedAmount, "blockMax": minedAmount,
               "usdEndMonth": float(0), "bgnEndMonth": float(0), "usdEquivalentToday": float(0),
               "bgnEquivalentToday": float(0)}
        obj["usdEndMonth"] = prices[minedMonthYear] * minedAmount
        obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
        obj["usdEquivalentToday"] = prices[minedMonthYear] * hydraPriceTodayUSD
        obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
        byMonth[minedMonthYear] = obj
        continue
    if minedMonthYear in byMonth:
        obj = byMonth[minedMonthYear]
        obj["total"] = obj["total"] + minedAmount
        obj["transactions"] = obj["transactions"] + 1
        obj["blockMin"] = minedAmount if minedAmount < obj["blockMin"] else obj["blockMin"]
        obj["blockMax"] = minedAmount if minedAmount > obj["blockMax"] else obj["blockMax"]
        obj["usdEndMonth"] = obj["total"] * prices[minedMonthYear]
        obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
        obj["usdEquivalentToday"] = obj["total"] * hydraPriceTodayUSD
        obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
        byMonth[minedMonthYear] = obj

print('Statistics by month:')
print(json.dumps(byMonth, indent=4))

totalMined = float(0)
totalTransactions = int(0)

for byMonthStatistic in byMonth:
    totalMined += byMonth[byMonthStatistic]["total"]
    totalTransactions += byMonth[byMonthStatistic]["transactions"]

print("")
print("Statistics overall:")
print("Mined: " + str(totalMined))
print("Transactions: " + str(totalTransactions))
print("USD Equivalent Today:" + str((totalMined * hydraPriceTodayUSD)))
print("BGN Equivalent Today:" + str((totalMined * hydraPriceTodayUSD) * usdToBGNRate))