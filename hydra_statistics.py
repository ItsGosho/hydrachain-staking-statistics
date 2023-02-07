import sys
import hydra_transactions_reader


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
The return dict key is a month in format month/year.
"""
def getMonthlyStakingStatistics(transactions):

    monthlyStakingStatistics = {}

    for transaction in transactions:

        if transaction.type != "Mined":
            continue

        month = str(transaction.date.month) + '/' + str(transaction.date.year)

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

transactions = hydra_transactions_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
result = getMonthlyStakingStatistics(transactions)
test = 5