import json
import sys
from calendar import monthrange
from datetime import datetime

import date_utils
import export_reader


class MonthlyStakingStatistic:

    def __init__(self,
                 yearMonth,
                 totalTransactions = 0,
                 totalIncomeHydra = 0,
                 lowestBlock = 0,
                 highestBlock = 0,
                 avgBlock = 0,
                 dailyIncomeHydra = 0,
                 dailyTransactions = 0
                 ):
        self.yearMonth = yearMonth
        self.totalTransactions = totalTransactions
        self.totalIncomeHydra = totalIncomeHydra
        self.lowestBlock = lowestBlock
        self.highestBlock = highestBlock
        self.avgBlock = avgBlock
        self.dailyIncomeHydra = dailyIncomeHydra
        self.dailyTransactions = dailyTransactions

    def __str__(self):
        return json.dumps(self.__dict__, default=str)
    def __unicode__(self):
        return json.dumps(self.__dict__, default=str)
    def __repr__(self):
        return json.dumps(self.__dict__, default=str)



"""
Create a monthly statistics of the provided transactions and returns a dict of MonthlyStakingStatistic objects.
Only information for Mined transactions will take place in the statistics.
The price is hydra's last day of the month price
Dict will be returned, where the key is a date in the provided dateFormat. Default is 06/2022 (%#m/%Y)
"""
def getMonthlyStakingStatistics(transactions):

    monthlyStakingStatistics = {}

    for transaction in transactions:

        if transaction.type != "Mined":
            continue

        yearMonth = date_utils.YearMonth(transaction.date.year, transaction.date.month)

        if yearMonth not in monthlyStakingStatistics:
            monthlyStakingStatistics[yearMonth] = MonthlyStakingStatistic(yearMonth=yearMonth)

        monthlyStakingStatistic = monthlyStakingStatistics[yearMonth]

        monthlyStakingStatistic.totalTransactions += 1
        monthlyStakingStatistic.totalIncomeHydra += transaction.amount

        currentLowestBlock = sys.maxsize if monthlyStakingStatistic.lowestBlock == 0 else monthlyStakingStatistic.lowestBlock
        currentHighestBlock = -sys.maxsize-1 if monthlyStakingStatistic.highestBlock == 0 else monthlyStakingStatistic.highestBlock

        monthlyStakingStatistic.lowestBlock = transaction.amount if transaction.amount < currentLowestBlock else currentLowestBlock
        monthlyStakingStatistic.highestBlock = transaction.amount if transaction.amount > currentHighestBlock else currentHighestBlock

        monthlyStakingStatistic.avgBlock = monthlyStakingStatistic.totalIncomeHydra / monthlyStakingStatistic.totalTransactions

        monthlyStakingStatistic.dailyTransactions = monthlyStakingStatistic.totalTransactions / yearMonth.getPassedDays()
        monthlyStakingStatistic.dailyIncomeHydra = monthlyStakingStatistic.totalIncomeHydra / yearMonth.getPassedDays()

    return monthlyStakingStatistics

#transactions = hydra_export_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
#result = getMonthlyStakingStatistics(transactions)
#test = 5