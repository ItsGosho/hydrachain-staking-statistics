import requests

url = 'https://api.exchangerate.host/2023-02-01'
response = requests.get(url)
data = response.json()

print(data)