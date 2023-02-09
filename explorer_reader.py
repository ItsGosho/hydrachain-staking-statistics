import json
from datetime import datetime

import requests

from export_reader import Transaction


def requestAddressTransactionIds(address, page=0, pageSize=20):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    url = f"https://explorer.hydrachain.org/7001/address/{address}/txs?page={page}&pageSize={pageSize}"
    response = requests.get(url=url, headers=headers)
    return response.json()


def requestTransactions(transactions):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.93 Safari/537.36'}
    url = f"https://explorer.hydrachain.org/7001/txs/{','.join(transactions)}"
    response = requests.get(url=url, headers=headers)
    return response.json()


def requestAllAddressTransactionIds(address):
    return requestAddressTransactionIds(address, 0, 1000000)


def requestAllAddressTransactions(address):

    addressTransactionIds = requestAllAddressTransactionIds(address)["transactions"]
    allAddressTransactions = []
    atTime = 20
    for j in range(0, len(addressTransactionIds), atTime):
        transactionIds = addressTransactionIds[j: j + atTime]
        transactions = requestTransactions(transactionIds)
        allAddressTransactions.extend(transactions)

    return allAddressTransactions

def readTransactions(address):
    transactions = requestAllAddressTransactions(address)

    formattedAndFilteredTransactions = []

    for transaction in transactions:

        if transaction['isCoinstake'] != True:
            continue

        confirmed = int(transaction['confirmations']) >= 2001
        date = datetime.fromtimestamp(transaction['timestamp']).date()
        type = 'Mined'
        label = ''
        address = ''
        amount = abs(float(transaction['fees'])) / 100000000
        id = transaction['id']

        transaction = Transaction(confirmed, date, type, label, address, amount, id)
        formattedAndFilteredTransactions.append(transaction)

    return formattedAndFilteredTransactions
