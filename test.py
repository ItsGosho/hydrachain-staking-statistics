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


def readTransactions():
    transactionsCSV = pandas.read_csv(r'C:\Users\itsgo\Desktop\hydra-export-1.csv')
    transactions = []

    for index, row in transactionsCSV.iterrows():
        confirmed = row['Confirmed']
        date = row['Date']
        type = row['Type']
        label = row['Label']
        address = row['Address']
        amount = row['Amount (HYDRA)']
        ID = row['ID']

        transaction = Transaction(confirmed, date, type, label, address, amount, ID)
        transactions.append(transaction)

    return transactions

transactions = readTransactions()

for transaction in transactions:

    print(str(transaction.confirmed) + ' ' +
              str(transaction.date) + ' ' +
                  str(transaction.type) + ' ' +
                      str(transaction.label) + ' ' +
                          str(transaction.address) + ' ' +
                              str(transaction.amount) + ' ' +
                                  str(transaction.id))
    print('-------')