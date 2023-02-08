from hydra_export_statistics import MonthlyStakingStatistic, getMonthlyStakingStatistics


class MonthlyStakingExtendedStatistics(MonthlyStakingStatistic):

    def __init__(self,
                 month='',
                 totalTransactions=0,
                 totalIncomeHydra=0,
                 lowestBlock=0,
                 highestBlock=0,
                 avgBlock=0,
                 hydraMonthEndPriceUSD=0,
                 incomeEndMonth=0,
                 incomeToday=0,
                 incomeDiff=0,
                 currency=0,
                 usdToCurrencyRate=0
                 ):
        super().__init__(month, totalTransactions, totalIncomeHydra, lowestBlock, highestBlock, avgBlock)
        self.hydraMonthEndPriceUSD = hydraMonthEndPriceUSD
        self.incomeEndMonth = incomeEndMonth
        self.incomeToday = incomeToday
        self.incomeDiff = incomeDiff
        self.currency = currency
        self.usdToCurrencyRate = usdToCurrencyRate

def getMonthlyStakingExtendedStatistics(monthlyStakingStatistics,
                                        hydraLastDayOfMonthPricesUSD,
                                        usdRatesLastDayOfMonth,
                                        hydraTodayPriceUSD,
                                        usdToSelectedCurrencyRateToday,
                                        selectedCurrency='USD'):

    monthlyStakingExtendedStatistics = {}

    for monthlyStakingStatisticDate in monthlyStakingStatistics:
        monthlyStakingStatistic = monthlyStakingStatistics[monthlyStakingStatisticDate]

        monthlyStakingExtendedStatistic = MonthlyStakingExtendedStatistics(
            month=monthlyStakingStatistic.month,
            totalTransactions=monthlyStakingStatistic.totalTransactions,
            totalIncomeHydra=monthlyStakingStatistic.totalIncomeHydra,
            lowestBlock=monthlyStakingStatistic.lowestBlock,
            highestBlock=monthlyStakingStatistic.highestBlock,
            avgBlock=monthlyStakingStatistic.avgBlock,
        )

        hydraMonthEndPriceUSD = hydraLastDayOfMonthPricesUSD[monthlyStakingStatisticDate]
        usdToSelectedCurrencyRate = usdRatesLastDayOfMonth[monthlyStakingStatisticDate][selectedCurrency]
        incomeEndMonth = monthlyStakingExtendedStatistic.totalIncomeHydra * hydraMonthEndPriceUSD * usdToSelectedCurrencyRate
        incomeToday = monthlyStakingExtendedStatistic.totalIncomeHydra * hydraTodayPriceUSD * usdToSelectedCurrencyRateToday
        incomeDiff = incomeToday - incomeEndMonth

        monthlyStakingExtendedStatistic.hydraMonthEndPriceUSD = hydraMonthEndPriceUSD
        monthlyStakingExtendedStatistic.incomeEndMonth = incomeEndMonth
        monthlyStakingExtendedStatistic.incomeToday = incomeToday
        monthlyStakingExtendedStatistic.incomeDiff = incomeDiff
        monthlyStakingExtendedStatistic.currency = selectedCurrency
        monthlyStakingExtendedStatistic.usdToCurrencyRate = usdToSelectedCurrencyRate

        monthlyStakingExtendedStatistics[monthlyStakingStatisticDate] = monthlyStakingExtendedStatistic

    return monthlyStakingExtendedStatistics

# WORKING_CURRENCY = 'BGN'
# transactions = hydra_export_reader.readTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
# usdToSelectedCurrencyRate = usd_rates.fetchCurrentUSDRates()[WORKING_CURRENCY]
# hydraPriceTodayUSD = hydra_prices.getCurrentHydraPrice()
# hydra_prices.synchronizeAllMonthsPricesForLastMonthDay()
# hydraLastDayOfMonthPrices = hydra_prices.getAllLastDayOfMonthPricesFormatted()
# usd_rates.synchronizeAllMonthsPricesForLastMonthDay()
# usdRatesLastDayOfMonth = usd_rates.getAllLastDayOfMonthPricesFormatted()
#
# monthlyStakingStatistics = getMonthlyStakingStatistics(transactions)
# monthlyStakingExtendedStatistics = getMonthlyStakingExtendedStatistics(monthlyStakingStatistics,
#                                                                        hydraLastDayOfMonthPrices,
#                                                                        usdRatesLastDayOfMonth,
#                                                                        hydraPriceTodayUSD,
#                                                                        usdToSelectedCurrencyRate,
#                                                                        WORKING_CURRENCY)
#
# let = 5