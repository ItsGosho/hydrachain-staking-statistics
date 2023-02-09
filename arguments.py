import argparse


class LogLevelAction(argparse.Action):
    def __call__(self, parser, namespace, logLevel, option_string=None):
        allowedLogLevels = ['NOTSET', 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']

        if logLevel not in allowedLogLevels:
            raise ValueError(
                'Log level {} is not supported. Supported ones: {}'.format(logLevel, ', '.join(allowedLogLevels)))

        setattr(namespace, self.dest, logLevel)


class CurrencyAction(argparse.Action):
    def __call__(self, parser, namespace, currency, option_string=None):
        allowedCurrencies = ['AED', 'AFN', 'ALL', 'AMD', 'ANG', 'AOA', 'ARS', 'AUD', 'AWG', 'AZN', 'BAM', 'BBD', 'BDT',
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

        if currency not in allowedCurrencies:
            raise ValueError(
                'Currency {} is not supported. Supported ones: {}'.format(currency, ', '.join(allowedCurrencies)))

        setattr(namespace, self.dest, currency)

class HydraChainArguments:

    def __init__(self):
        self.initiailize()

    def initiailize(self):
        parser = argparse.ArgumentParser(description='Hydrachain Staking Statistics')

        parser.add_argument('--csv-file-path', dest='csv-file-path', type=str,
                            help='Absolute path to the CSV export file from the Hydra GUI.',
                            required=True)
        parser.add_argument('--currency', dest='currency', type=str,
                            help='Currency to be shown is the statistic tables. Default is USD', default='USD',
                            action=CurrencyAction)
        parser.add_argument('--log-level', dest='log-level', type=str,
                            help='Level of logging. Default is INFO', default='INFO', action=LogLevelAction)

        self.parser = parser
        self.arguments = self.parser.parse_args()

    def getCSVFilePath(self):
        return self.arguments.__getattribute__('csv-file-path')

    def getCurrency(self):
        return self.arguments.__getattribute__('currency')

    def getLogLevel(self):
        return self.arguments.__getattribute__('log-level')
