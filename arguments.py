import argparse

LOG_LEVEL_DEFAULT = 'INFO'
CURRENCY_DEFAULT = 'USD'

CSV_FILE_PATH_NAME = 'csv-file-path'
CURRENCY_NAME = 'currency'
LOG_LEVEL_NAME = 'log-level'

CURRENCY_ALLOWED = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT',
                             'BGN', 'BHD', 'BIF', 'BMD', 'BND', 'BOB', 'BRL', 'BSD', 'BTC', 'BTN', 'BWP', 'BYN', 'BZD',
                             'CAD', 'CDF', 'CHF', 'CLF', 'CLP', 'CNH', 'CNY', 'COP', 'CRC', 'CUC', 'CUP', 'CVE', 'CZK',
                             'DJF', 'DKK', 'DOP', 'DZD', 'EGP', 'ERN', 'ETB', 'EUR', 'FJD', 'FKP', 'GBP', 'GEL', 'GGP',
                             'GHS', 'GIP', 'GMD', 'GNF', 'GTQ', 'GYD', 'HKD', 'HNL', 'HRK', 'HTG', 'HUF', 'IDR', 'ILS',
                             'IMP', 'INR', 'IQD', 'IRR', 'ISK', 'JEP', 'JMD', 'JOD', 'JPY', 'KES', 'KGS', 'KHR', 'KMF',
                             'KPW', 'KRW', 'KWD', 'KYD', 'KZT', 'LAK', 'LBP', 'LKR', 'LRD', 'LSL', 'LYD', 'MAD', 'MDL',
                             'MGA', 'MKD', 'MMK', 'MNT', 'MOP', 'MRU', 'MUR', 'MVR', 'MWK', 'MXN', 'MYR', 'MZN', 'NAD',
                             'NGN', 'NIO', 'NOK', 'NPR', 'NZD', 'OMR', 'PAB', 'PEN', 'PGK', 'PHP', 'PKR', 'PLN', 'PYG',
                             'QAR', 'RON', 'RSD', 'RUB', 'RWF', 'SAR', 'SBD', 'SCR', 'SDG', 'SEK', 'SGD', 'SHP', 'SLL',
                             'SOS', 'SRD', 'SSP', 'STD', 'STN', 'SVC', 'SYP', 'SZL', 'THB', 'TJS', 'TMT', 'TND', 'TOP',
                             'TRY', 'TTD', 'TWD', 'TZS', 'UAH', 'UGX', 'USD', 'UYU', 'UZS', 'VES', 'VND', 'VUV', 'WST',
                             'XAF', 'XAG', 'XAU', 'XCD', 'XDR', 'XOF', 'XPD', 'XPF', 'XPT', 'YER', 'ZAR', 'ZMW', 'ZWL']

LOG_LEVEL_ALLOWED = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']


class LogLevelAction(argparse.Action):
    def __call__(self, parser, namespace, logLevel, option_string=None):

        if logLevel not in LOG_LEVEL_ALLOWED:
            raise ValueError(
                'Log level {} is not supported. Supported ones: {}'.format(logLevel, ', '.join(LOG_LEVEL_ALLOWED)))

        setattr(namespace, self.dest, logLevel)


class CurrencyAction(argparse.Action):
    def __call__(self, parser, namespace, currency, option_string=None):

        if currency not in CURRENCY_ALLOWED:
            raise ValueError(
                'Currency {} is not supported. Supported ones: {}'.format(currency, ', '.join(CURRENCY_ALLOWED)))

        setattr(namespace, self.dest, currency)


class HydraChainArguments:

    def __init__(self):
        self.initiailize()

    def initiailize(self):
        parser = argparse.ArgumentParser(description='Hydrachain Staking Statistics')

        parser.add_argument('--csv-file-path',
                            dest=CSV_FILE_PATH_NAME,
                            type=str,
                            help='Absolute path to the CSV export file from the Hydra GUI.',
                            required=True)

        parser.add_argument('--currency',
                            dest=CURRENCY_NAME,
                            type=str,
                            help='Currency to be shown is the statistic tables. Default is {}'.format(CURRENCY_DEFAULT),
                            default=CURRENCY_DEFAULT,
                            action=CurrencyAction)

        parser.add_argument('--log-level',
                            dest=LOG_LEVEL_NAME,
                            type=str,
                            help='Level of logging. Default is {}'.format(LOG_LEVEL_DEFAULT),
                            default=LOG_LEVEL_DEFAULT,
                            action=LogLevelAction)

        self.parser = parser
        self.arguments = self.parser.parse_args()

    def getCSVFilePath(self):
        return self.getArgument(CSV_FILE_PATH_NAME)

    def getCurrency(self):
        return self.getArgument(CURRENCY_NAME)

    def getLogLevel(self):
        return self.getArgument(LOG_LEVEL_NAME)

    def getArgument(self, argumentName):
        return self.arguments.__getattribute__(argumentName)

    def getArguments(self):
        return self.arguments
