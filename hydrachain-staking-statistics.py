import re
import json
import hydra_transactions_reader
import hydra_prices
from prettytable import PrettyTable as pt

transactions = hydra_transactions_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
usdToBGNRate = float(1.80)  # TODO:
hydraPriceTodayUSD = hydra_prices.getCurrentHydraPrice()
hydra_prices.synchronizeAllMonthsPricesForLastMonthDay()
prices = hydra_prices.getAllLastDayOfMonthPricesFormatted()

byMonths = {}
tableMontlyStakingStatistics = pt(title="Monthly Staking Statistics")
tableMontlyStakingStatistics.field_names = ["Month", "Mined", "Transactions", "Lowest Block", "Highest Block",
                                            "Month End USD", "Month End BGN",
                                            "Today USD", "Today BGN"]
tableMontlyStakingStatistics.align = "r"

for transaction in transactions:

    if transaction.type != "Mined":
        continue

    minedMonthYear = str(transaction.date.month) + '/' + str(transaction.date.year)
    minedAmount = float(transaction.amount)

    if minedMonthYear not in byMonths:
        obj = {"total": minedAmount, "transactions": int(1), "blockMin": minedAmount, "blockMax": minedAmount,
               "usdEndMonth": float(0), "bgnEndMonth": float(0), "usdEquivalentToday": float(0),
               "bgnEquivalentToday": float(0)}
        obj["usdEndMonth"] = prices[minedMonthYear] * minedAmount
        obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
        obj["usdEquivalentToday"] = prices[minedMonthYear] * hydraPriceTodayUSD
        obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
        byMonths[minedMonthYear] = obj
        continue
    if minedMonthYear in byMonths:
        obj = byMonths[minedMonthYear]
        obj["total"] = obj["total"] + minedAmount
        obj["transactions"] = obj["transactions"] + 1
        obj["blockMin"] = minedAmount if minedAmount < obj["blockMin"] else obj["blockMin"]
        obj["blockMax"] = minedAmount if minedAmount > obj["blockMax"] else obj["blockMax"]
        obj["usdEndMonth"] = obj["total"] * prices[minedMonthYear]
        obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
        obj["usdEquivalentToday"] = obj["total"] * hydraPriceTodayUSD
        obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
        byMonths[minedMonthYear] = obj

for byMonth in byMonths:
    tableMontlyStakingStatistics.add_row([
        byMonth,
        round(byMonths[byMonth]["total"], 2),
        byMonths[byMonth]["transactions"],
        round(byMonths[byMonth]["blockMin"], 2),
        round(byMonths[byMonth]["blockMax"], 2),
        round(byMonths[byMonth]["usdEndMonth"], 2),
        round(byMonths[byMonth]["bgnEndMonth"], 2),
        round(byMonths[byMonth]["usdEquivalentToday"], 2),
        round(byMonths[byMonth]["bgnEquivalentToday"], 2),
    ])

print(tableMontlyStakingStatistics)

totalMined = float(0)
totalTransactions = int(0)

for byMonthStatistic in byMonths:
    totalMined += byMonths[byMonthStatistic]["total"]
    totalTransactions += byMonths[byMonthStatistic]["transactions"]

tableOverallStakingStatistics = pt(title="Overall Staking Statistics")
tableOverallStakingStatistics.field_names = ["Mined", "Transactions", "Today USD", "Today BGN"]
tableOverallStakingStatistics.align = "r"
tableOverallStakingStatistics.add_row([
    totalMined,
    totalTransactions,
    (totalMined * hydraPriceTodayUSD),
    (totalMined * hydraPriceTodayUSD) * usdToBGNRate
])

print(tableOverallStakingStatistics)
