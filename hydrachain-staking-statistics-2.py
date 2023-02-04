import re
import json
import hydra_transactions_reader

transactions = hydra_transactions_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')

for transaction in transactions:

    minedMonthYear = str(transaction.date.month) + '/' + str(transaction.date.year - 2000)
    minedDate = str(transaction.date.day) + '/' + str(transaction.date.month) + '/' + str(transaction.date.year - 2000)
    minedHour = str(transaction.date.hour)
    minedAmount = float(transaction.amount)

    # if minedMonthYear not in byMonth:
    #     obj = {"total": minedAmount, "transactions": int(1), "blockMin": minedAmount, "blockMax": minedAmount,
    #            "usdEndMonth": float(0), "bgnEndMonth": float(0), "usdEquivalentToday": float(0),
    #            "bgnEquivalentToday": float(0)}
    #     obj["usdEndMonth"] = prices[minedMonthYear] * minedAmount
    #     obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
    #     obj["usdEquivalentToday"] = prices[minedMonthYear] * hydraPriceTodayUSD
    #     obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
    #     byMonth[minedMonthYear] = obj
    #     continue
    # if minedMonthYear in byMonth:
    #     obj = byMonth[minedMonthYear];
    #     obj["total"] = obj["total"] + minedAmount
    #     obj["transactions"] = obj["transactions"] + 1
    #     obj["blockMin"] = minedAmount if minedAmount < obj["blockMin"] else obj["blockMin"]
    #     obj["blockMax"] = minedAmount if minedAmount > obj["blockMax"] else obj["blockMax"]
    #     obj["usdEndMonth"] = obj["total"] * prices[minedMonthYear]
    #     obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
    #     obj["usdEquivalentToday"] = obj["total"] * hydraPriceTodayUSD
    #     obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
    #     byMonth[minedMonthYear] = obj

    print(str(transaction.confirmed) + ' ' +
              str(transaction.date) + ' ' +
                  str(transaction.type) + ' ' +
                      str(transaction.label) + ' ' +
                          str(transaction.address) + ' ' +
                              str(transaction.amount) + ' ' +
                                  str(transaction.id))
    print('-------')

test = 5