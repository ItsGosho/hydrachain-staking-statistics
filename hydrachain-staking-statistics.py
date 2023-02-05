import re
import json
import hydra_transactions_reader
import hydra_prices
import usd_rates
from prettytable import PrettyTable as pt
import logging

logging.basicConfig(level = logging.INFO)
WORKING_CURRENCY = "BGN"

transactions = hydra_transactions_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
usdToSelectedCurrencyRate = usd_rates.fetchCurrentUSDRates()[WORKING_CURRENCY]
hydraPriceTodayUSD = hydra_prices.getCurrentHydraPrice()
hydra_prices.synchronizeAllMonthsPricesForLastMonthDay()
hydraLastDayOfMonthPrices = hydra_prices.getAllLastDayOfMonthPricesFormatted()
usd_rates.synchronizeAllMonthsPricesForLastMonthDay()
usdRatesLastDayOfMonth = usd_rates.getAllLastDayOfMonthPricesFormatted()

byMonths = {}
tableMontlyStakingStatistics = pt(title="Monthly Staking Statistics")
tableMontlyStakingStatistics.field_names = [
    "Month",
    "Transactions",
    "Mined",
    "Month End Price USD",
    "Month End {}".format(WORKING_CURRENCY),
    "Today {}".format(WORKING_CURRENCY),
    "Diff {}".format(WORKING_CURRENCY),
    "Lowest Block",
    "Highest Block",
    "Avg Block"
]
tableMontlyStakingStatistics.align = "r"

for transaction in transactions:

    if transaction.type != "Mined":
        continue

    minedMonthYear = str(transaction.date.month) + '/' + str(transaction.date.year)
    minedAmount = float(transaction.amount)

    if minedMonthYear not in byMonths:
        obj = {"total": minedAmount, "transactions": int(1), "blockMin": minedAmount, "blockMax": minedAmount,
               "usdEndMonth": float(0), "usdEquivalentToday": float(0)}
        obj["usdEndMonth"] = hydraLastDayOfMonthPrices[minedMonthYear] * minedAmount
        obj["usdEquivalentToday"] = hydraLastDayOfMonthPrices[minedMonthYear] * hydraPriceTodayUSD
        byMonths[minedMonthYear] = obj
        continue
    if minedMonthYear in byMonths:
        obj = byMonths[minedMonthYear]
        obj["total"] = obj["total"] + minedAmount
        obj["transactions"] = obj["transactions"] + 1
        obj["blockMin"] = minedAmount if minedAmount < obj["blockMin"] else obj["blockMin"]
        obj["blockMax"] = minedAmount if minedAmount > obj["blockMax"] else obj["blockMax"]
        obj["usdEndMonth"] = obj["total"] * hydraLastDayOfMonthPrices[minedMonthYear]
        obj["usdEquivalentToday"] = obj["total"] * hydraPriceTodayUSD
        byMonths[minedMonthYear] = obj

for byMonth in byMonths:
    usdEndMonth = round(byMonths[byMonth]["usdEndMonth"], 2)
    usdToday = round(byMonths[byMonth]["usdEquivalentToday"], 2)
    transactions = byMonths[byMonth]["transactions"]
    total = round(byMonths[byMonth]["total"], 2)
    selectedCurrencyEndMonth = usdEndMonth * usdToSelectedCurrencyRate
    selectedCurrencyToday = usdToday * usdToSelectedCurrencyRate

    percentageIncreaseMonthEndTodayUSD = (selectedCurrencyToday - selectedCurrencyEndMonth)
    tableMontlyStakingStatistics.add_row([
        byMonth,
        transactions,
        total,
        round(hydraLastDayOfMonthPrices[byMonth], 2),
        round(selectedCurrencyEndMonth, 2),
        round(selectedCurrencyToday, 2),
        str(round(percentageIncreaseMonthEndTodayUSD, 2)),
        round(byMonths[byMonth]["blockMin"], 2),
        round(byMonths[byMonth]["blockMax"], 2),
        round(total / transactions, 2)
    ])

print(tableMontlyStakingStatistics)

totalMined = float(0)
totalTransactions = int(0)

for byMonthStatistic in byMonths:
    totalMined += byMonths[byMonthStatistic]["total"]
    totalTransactions += byMonths[byMonthStatistic]["transactions"]

tableOverallStakingStatistics = pt(title="Overall Staking Statistics")
tableOverallStakingStatistics.field_names = ["Transactions","Mined", "Today {}".format(WORKING_CURRENCY)]
tableOverallStakingStatistics.align = "r"
tableOverallStakingStatistics.add_row([
    totalTransactions,
    round(totalMined, 2),
    round(totalMined * hydraPriceTodayUSD * usdToSelectedCurrencyRate, 2),
])

print(tableOverallStakingStatistics)
