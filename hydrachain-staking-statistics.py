import hydra_export_reader
import hydra_export_statistics
import hydra_prices
import usd_rates
from prettytable import PrettyTable as pt
import logging
import hydra_extended_statistics
import arguments

hydrachainArguments = arguments.HydraChainArguments()

logging.basicConfig(level=hydrachainArguments.getLogLevel())
logging.debug('Provided arguments %s', hydrachainArguments.getArguments())

currency = hydrachainArguments.getCurrency()
transactions = hydra_export_reader.readTransactions(hydrachainArguments.getCSVFilePath())
logging.debug('Read transactions %s', transactions)

usdToSelectedCurrencyRate = usd_rates.fetchCurrentUSDRates()[currency]
hydraPriceTodayUSD = hydra_prices.getCurrentHydraPrice()
hydra_prices.synchronizeAllMonthsPricesForLastMonthDay()
hydraLastDayOfMonthPrices = hydra_prices.getAllLastDayOfMonthPricesFormatted()
usd_rates.synchronizeAllMonthsPricesForLastMonthDay()
usdRatesLastDayOfMonth = usd_rates.getAllLastDayOfMonthPricesFormatted()

monthlyStakingStatistics = hydra_export_statistics.getMonthlyStakingStatistics(transactions)
monthlyStakingExtendedStatistics = hydra_extended_statistics.getMonthlyStakingExtendedStatistics(
    monthlyStakingStatistics,
    hydraLastDayOfMonthPrices,
    usdRatesLastDayOfMonth,
    hydraPriceTodayUSD,
    usdToSelectedCurrencyRate,
    currency)

totalTransactionsOverall = 0
totalIncomeHydraOverall = 0

tableMontlyStakingStatistics = pt(title="Monthly Staking Statistics")
tableMontlyStakingStatistics.field_names = [
    "Month",
    "Transactions",
    "Mined",
    "Month End Price USD",
    "Month End {}".format(currency),
    "Today {}".format(currency),
    "Diff {}".format(currency),
    "Lowest Block",
    "Highest Block",
    "Avg Block"
]
tableMontlyStakingStatistics.align = "r"

for monthlyStakingExtendedStatisticDate in monthlyStakingExtendedStatistics:
    monthlyStakingExtendedStatistic = monthlyStakingExtendedStatistics[monthlyStakingExtendedStatisticDate]

    totalTransactionsOverall += monthlyStakingExtendedStatistic.totalTransactions
    totalIncomeHydraOverall += monthlyStakingExtendedStatistic.totalIncomeHydra

    tableMontlyStakingStatistics.add_row([
        monthlyStakingExtendedStatisticDate,
        monthlyStakingExtendedStatistic.totalTransactions,
        round(monthlyStakingExtendedStatistic.totalIncomeHydra, 2),
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

#Overall Staking Statistics

tableOverallStakingStatistics = pt(title="Overall Staking Statistics")
tableOverallStakingStatistics.field_names = ["Transactions", "Mined", "Today {}".format(currency)]
tableOverallStakingStatistics.align = "r"
tableOverallStakingStatistics.add_row([
    totalTransactionsOverall,
    round(totalIncomeHydraOverall, 2),
    round(totalIncomeHydraOverall * hydraPriceTodayUSD * usdToSelectedCurrencyRate, 2),
])

print(tableOverallStakingStatistics)
