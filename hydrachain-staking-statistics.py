import export_reader
import explorer_reader
import export_statistics
import prices
import rates
from prettytable import PrettyTable as pt
import logging
import extended_statistics
import arguments

LOG_FORMAT = '[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'
HYDRACHAIN_STAKING_STATISTICS_VERSION = '2.0.0'

hydrachainArguments = arguments.HydraChainArguments()

logging.basicConfig(level=hydrachainArguments.getLogLevel(), format=LOG_FORMAT)
logging.info("Hydrachain Staking Statistics v%s", HYDRACHAIN_STAKING_STATISTICS_VERSION)
logging.debug('Provided arguments %s', hydrachainArguments.getArguments())

transactions = []

if hydrachainArguments.hasAddress():
    transactions = explorer_reader.readTransactions(hydrachainArguments.getAddress())
elif hydrachainArguments.hasCSVFilePath():
    transactions = export_reader.readTransactions(hydrachainArguments.getCSVFilePath())
else:
    transactions = []

logging.debug('Read transactions %s', transactions)

currency = hydrachainArguments.getCurrency()
usdToSelectedCurrencyRate = rates.fetchCurrentUSDRates()[currency]
logging.debug('Fetched usd to selected currency rates for selected currency %s are %s', currency,
              usdToSelectedCurrencyRate)

hydraPriceTodayUSD = prices.getCurrentHydraPrice()
logging.debug('Hydra price today is %s', hydraPriceTodayUSD)

prices.synchronizeAllMonthsPricesForLastMonthDay()
hydraLastDayOfMonthPrices = prices.getAllLastDayOfMonthPricesFormatted()
logging.debug('All hydra last day of month prices formatted %s', hydraLastDayOfMonthPrices)

rates.synchronizeAllMonthsPricesForLastMonthDay()
usdRatesLastDayOfMonth = rates.getAllLastDayOfMonthPricesFormatted()
logging.debug('All usd rates last day of month formatted %s', hydraLastDayOfMonthPrices)

monthlyStakingStatistics = export_statistics.getMonthlyStakingStatistics(transactions)
logging.debug('Monthly staking statistics: %s', hydraLastDayOfMonthPrices)

monthlyStakingExtendedStatistics = extended_statistics.getMonthlyStakingExtendedStatistics(
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
    "Daily Transactions",
    "Daily Mined",
    "Hydra Monthly Price",
    "Income Monthly {}".format(currency),
    "Income Today ({:.2f} {})".format(hydraPriceTodayUSD * usdToSelectedCurrencyRate, currency),
    "Income Change {}".format(currency),
    "Lowest Block",
    "Highest Block",
    "Avg Block"
]
tableMontlyStakingStatistics.align = "r"

for monthlyStakingExtendedStatisticDate in monthlyStakingExtendedStatistics:
    monthlyStakingExtendedStatistic = monthlyStakingExtendedStatistics[monthlyStakingExtendedStatisticDate]

    totalTransactionsOverall += monthlyStakingExtendedStatistic.totalTransactions
    totalIncomeHydraOverall += monthlyStakingExtendedStatistic.totalIncomeHydra
    isTodayMonthAndYear = monthlyStakingExtendedStatisticDate.isTodayMonthAndYear()

    tableMontlyStakingStatistics.add_row([
        "{}/{}{}".format(monthlyStakingExtendedStatisticDate.month, monthlyStakingExtendedStatisticDate.year, "*" if isTodayMonthAndYear else ""),
        monthlyStakingExtendedStatistic.totalTransactions,
        "{:.2f}".format(monthlyStakingExtendedStatistic.totalIncomeHydra),
        "{:.2f}".format(monthlyStakingExtendedStatistic.dailyTransactions),
        "{:.2f}".format(monthlyStakingExtendedStatistic.dailyIncomeHydra),
        "{:.2f}$".format(monthlyStakingExtendedStatistic.hydraMonthEndPriceUSD) if monthlyStakingExtendedStatistic.hydraMonthEndPriceUSD != 0 and not isTodayMonthAndYear else "-",
        "{:.2f}".format(monthlyStakingExtendedStatistic.incomeEndMonth) if monthlyStakingExtendedStatistic.incomeEndMonth != 0 and not isTodayMonthAndYear else "-",
        "{:.2f}".format(monthlyStakingExtendedStatistic.incomeToday),
        "{:.2f}".format(monthlyStakingExtendedStatistic.incomeDiff) if monthlyStakingExtendedStatistic.incomeDiff != 0 and not isTodayMonthAndYear else "-",
        "{:.2f}".format(monthlyStakingExtendedStatistic.lowestBlock),
        "{:.2f}".format(monthlyStakingExtendedStatistic.highestBlock),
        "{:.2f}".format(monthlyStakingExtendedStatistic.avgBlock)
    ])
    pass

print(tableMontlyStakingStatistics)

# Overall Staking Statistics

tableOverallStakingStatistics = pt(title="Overall Staking Statistics")
tableOverallStakingStatistics.field_names = ["Transactions", "Mined", "Today {}".format(currency)]
tableOverallStakingStatistics.align = "r"
tableOverallStakingStatistics.add_row([
    totalTransactionsOverall,
    round(totalIncomeHydraOverall, 2),
    round(totalIncomeHydraOverall * hydraPriceTodayUSD * usdToSelectedCurrencyRate, 2),
])

print(tableOverallStakingStatistics)
