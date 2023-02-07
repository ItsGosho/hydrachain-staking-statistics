import sys

import hydra_export_reader


class MonthlyStakingStatistic:

    def __init__(self, month):
        self.month = month
        self.totalTransactions = 0
        self.totalIncomeHydra = 0
        self.lowestBlock = 0
        self.highestBlock = 0

"""
Create a monthly statistics of the provided transactions and returns a dict of MonthlyStakingStatistic objects.
Only information for Mined transactions will take place in the statistics.
The price is hydra's last day of the month price
Dict will be returned, where the key is a date in the provided dateFormat. Default is 06/2022 (%#m/%Y)
"""
def getMonthlyStakingStatistics(transactions, dateFormat = '%#m/%Y'):

    monthlyStakingStatistics = {}

    for transaction in transactions:

        if transaction.type != "Mined":
            continue

        month = transaction.date.strftime(dateFormat)

        if month not in monthlyStakingStatistics:
            monthlyStakingStatistics[month] = MonthlyStakingStatistic(month)

        monthlyStakingStatistic = monthlyStakingStatistics[month]

        monthlyStakingStatistic.totalTransactions += 1
        monthlyStakingStatistic.totalIncomeHydra += transaction.amount

        currentLowestBlock = sys.maxsize if monthlyStakingStatistic.lowestBlock == 0 else monthlyStakingStatistic.lowestBlock
        currentHighestBlock = sys.maxsize if monthlyStakingStatistic.highestBlock == 0 else monthlyStakingStatistic.highestBlock

        monthlyStakingStatistic.lowestBlock = transaction.amount if transaction.amount < currentLowestBlock else currentLowestBlock
        monthlyStakingStatistic.highestBlock = transaction.amount if transaction.amount < currentHighestBlock else currentHighestBlock

    return monthlyStakingStatistics

#transactions = hydra_export_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
#result = getMonthlyStakingStatistics(transactions)
#test = 5