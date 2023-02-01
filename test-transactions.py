import hydra_transactions_reader

path = r'C:\Users\itsgo\Desktop\hydra-export-1.csv'
transactions = hydra_transactions_reader.readTransactions(path)

for transaction in transactions:

    print(str(transaction.confirmed) + ' ' +
              str(transaction.date) + ' ' +
                  str(transaction.type) + ' ' +
                      str(transaction.label) + ' ' +
                          str(transaction.address) + ' ' +
                              str(transaction.amount) + ' ' +
                                  str(transaction.id))
    print('-------')