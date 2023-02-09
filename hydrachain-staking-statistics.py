import hydra_export_reader
import hydra_export_statistics
import hydra_prices
import usd_rates
from prettytable import PrettyTable as pt
import logging
import hydra_extended_statistics
import arguments

hydrachainArguments = arguments.HydraChainArguments()

logging.basicConfig(level=hydrachainArguments.getLogLevel(), format='[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s')
logging.debug('Provided arguments %s', hydrachainArguments.getArguments())

currency = hydrachainArguments.getCurrency()
transactions = hydra_export_reader.readTransactions(hydrachainArguments.getCSVFilePath())
logging.debug('Read transactions %s', transactions)

usdToSelectedCurrencyRate = usd_rates.fetchCurrentUSDRates()[currency]
logging.debug('Fetched usd to selected currency rates for selected currency %s are %s', currency, usdToSelectedCurrencyRate)

hydraPriceTodayUSD = hydra_prices.getCurrentHydraPrice()
logging.debug('Hydra price today is %s', hydraPriceTodayUSD)

hydra_prices.synchronizeAllMonthsPricesForLastMonthDay()
hydraLastDayOfMonthPrices = hydra_prices.getAllLastDayOfMonthPricesFormatted()
logging.debug('All hydra last day of month prices formatted %s', hydraLastDayOfMonthPrices)

usd_rates.synchronizeAllMonthsPricesForLastMonthDay()
usdRatesLastDayOfMonth = usd_rates.getAllLastDayOfMonthPricesFormatted()
logging.debug('All usd rates last day of month formatted %s', hydraLastDayOfMonthPrices)

monthlyStakingStatistics = hydra_export_statistics.getMonthlyStakingStatistics(transactions)
logging.debug('Monthly staking statistics: %s', hydraLastDayOfMonthPrices)

monthlyStakingExtendedStatistics = hydra_extended_statistics.getMonthlyStakingExtendedStatistics(
    monthlyStakingStatistics,
    hydraLastDayOfMonthPrices,
    usdRatesLastDayOfMonth,
    hydraPriceTodayUSD,
    usdToSelectedCurrencyRate,
    currency)
logging.debug('Monthly staking extended statistics: %s', monthlyStakingExtendedStatistics)

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
