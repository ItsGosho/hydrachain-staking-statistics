import json

import pandas
from datetime import datetime

class Transaction:
    def __init__(self, confirmed, date, type, label, address, amount, id):
        self.confirmed = confirmed
        self.date = date
        self.type = type
        self.label = label
        self.address = address
        self.amount = amount
        self.id = id

    def __str__(self):
        return json.dumps(self.__dict__, default=str)
    def __unicode__(self):
        return json.dumps(self.__dict__, default=str)
    def __repr__(self):
        return json.dumps(self.__dict__, default=str)

def readTransactions(csvFilePath):
    transactionsCSV = pandas.read_csv(csvFilePath)
    transactions = []

    for index, row in transactionsCSV.iterrows():

        transaction = _parseTransactionCSVRow(row)
        transactions.append(transaction)

    return transactions

def _parseTransactionCSVRow(row):
    confirmed = bool(row['Confirmed'])
    date = datetime.strptime(row['Date'], '%Y-%m-%dT%H:%M:%S')
    type = row['Type']
    label = row['Label']
    address = row['Address']
    amount = float(row['Amount (HYDRA)'])
    ID = row['ID']

    return Transaction(confirmed, date, type, label, address, amount, ID)

#test = readMinedTransactions(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
#print(test)