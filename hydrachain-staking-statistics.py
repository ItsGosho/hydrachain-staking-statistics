import re
import json
import hydra_export_reader
import hydra_export_statistics
import hydra_prices
import usd_rates
from prettytable import PrettyTable as pt
import logging
import hydra_extended_statistics

logging.basicConfig(level=logging.INFO)
WORKING_CURRENCY = "BGN"

transactions = hydra_export_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
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

monthlyStakingStatistics = hydra_export_statistics.getMonthlyStakingStatistics(transactions)
monthlyStakingExtendedStatistics = hydra_extended_statistics.getMonthlyStakingExtendedStatistics(monthlyStakingStatistics,
                                                                       hydraLastDayOfMonthPrices,
                                                                       usdRatesLastDayOfMonth,
                                                                       hydraPriceTodayUSD,
                                                                       usdToSelectedCurrencyRate,
                                                                       WORKING_CURRENCY)

for monthlyStakingExtendedStatisticDate in monthlyStakingExtendedStatistics:
    monthlyStakingExtendedStatistic = monthlyStakingExtendedStatistics[monthlyStakingExtendedStatisticDate]

    tableMontlyStakingStatistics.add_row([
        monthlyStakingExtendedStatisticDate,
        monthlyStakingExtendedStatistic.totalTransactions,
        monthlyStakingExtendedStatistic.totalIncomeHydra,
        round(monthlyStakingExtendedStatistic.hydraMonthEndPriceUSD, 2),
        round(monthlyStakingExtendedStatistic.incomeEndMonth, 2),
        round(monthlyStakingExtendedStatistic.incomeToday, 2),
        str(round(monthlyStakingExtendedStatistic.incomeDiff, 2)),
        round(monthlyStakingExtendedStatistic.lowestBlock, 2),
        round(monthlyStakingExtendedStatistic.highestBlock, 2),
        round(monthlyStakingExtendedStatistic.avgBlock, 2)
    ])
    pass

print(tableMontlyStakingStatistics)

# totalMined = float(0)
# totalTransactions = int(0)
#
# for byMonthStatistic in byMonths:
#     totalMined += byMonths[byMonthStatistic]["total"]
#     totalTransactions += byMonths[byMonthStatistic]["transactions"]
#
# tableOverallStakingStatistics = pt(title="Overall Staking Statistics")
# tableOverallStakingStatistics.field_names = ["Transactions", "Mined", "Today {}".format(WORKING_CURRENCY)]
# tableOverallStakingStatistics.align = "r"
# tableOverallStakingStatistics.add_row([
#     totalTransactions,
#     round(totalMined, 2),
#     round(totalMined * hydraPriceTodayUSD * usdToSelectedCurrencyRate, 2),
# ])
#
# print(tableOverallStakingStatistics)
