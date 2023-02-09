import json

import requests

# ADDRESS = "H8Rw6bdg8zYgQ8YYm5K7zkK6EytetYsAuY"
ADDRESS = "H7FYCLijimtbYk7gdN1hmweftuWLQni3m5"


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


transactionIds = requestAddressTransactionIds(ADDRESS, 0, 1000000)["transactions"]
transactions = requestTransactions(transactionIds)
print(json.dumps(transactions, indent=4))
