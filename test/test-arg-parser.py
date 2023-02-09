import argparse

parser = argparse.ArgumentParser(description='Hydrachain Staking Statistics')
parser.add_argument('--csv', dest='csv', type=str, help='Absolute path to the CSV export file from the Hydra GUI.', required=True)
parser.add_argument('--currency', dest='currency', type=str,
                    help='Currency to be shown is the statistic tables. Default is USD', default='USD')
parser.add_argument('--log-level', dest='log-level', type=str,
                    help='Level of logging. Default is INFO', default='INFO')

args = parser.parse_args()
print(args.__getattribute__('csv'))
print(args.__getattribute__('currency'))
print(args.__getattribute__('log-level'))
