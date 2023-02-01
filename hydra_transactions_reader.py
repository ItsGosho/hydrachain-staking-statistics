import pandas

class Transaction:
    def __init__(self, confirmed, date, type, label, address, amount, id):
        self.confirmed = confirmed
        self.date = date
        self.type = type
        self.label = label
        self.address = address
        self.amount = amount
        self.id = id

def readTransactions(csvFilePath):
    transactionsCSV = pandas.read_csv(csvFilePath)
    transactions = []

    for index, row in transactionsCSV.iterrows():

        transaction = parseTransactionCSVRow(row)
        transactions.append(transaction)

    return transactions

def parseTransactionCSVRow(row):
    confirmed = row['Confirmed']
    date = row['Date']
    type = row['Type']
    label = row['Label']
    address = row['Address']
    amount = row['Amount (HYDRA)']
    ID = row['ID']

    transaction = Transaction(confirmed, date, type, label, address, amount, ID)
    return transaction