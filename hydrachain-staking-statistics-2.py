import re
import json
import hydra_transactions_reader

hydraTransactions = hydra_transactions_reader.readTransactions('C:\Users\itsgo\Desktop\hydra-export-1.csv')
usdToBGNRate = float(1.80)
hydraPriceTodayUSD = float(2.00)
byMonth = {}
prices = {} #By month at the end of the month in usd
prices['1/23'] = float(2.00)
prices['12/22'] = float(1.48)
prices['11/22'] = float(1.60)
prices['10/22'] = float(2.62)
prices['9/22'] = float(2.09)
prices['8/22'] = float(2.74)
prices['7/22'] = float(2.98)
prices['6/22'] = float(2.44)
prices['5/22'] = float(3.85)
prices['4/22'] = float(6.88)
prices['3/22'] = float(8.76)
prices['2/22'] = float(7.27)
prices['1/22'] = float(8.25)
prices['12/21'] = float(8.01)
prices['11/21'] = float(13.25)
prices['10/21'] = float(17.24)
prices['9/21'] = float(18.04)
prices['8/21'] = float(18.18)
prices['7/21'] = float(16.80)
prices['6/21'] = float(28.42)

for fileLine in file:
    fileLineRegexSplit = re.split('([a-z0-9]+)([\/])([a-z0-9]+)([\/])([a-z0-9]+)(\s+)([0-9\:]+)(\s+)([0-9.]+)', fileLine)
    
    if(len(fileLineRegexSplit) < 11):
      continue
    
    minedMonthYear = fileLineRegexSplit[1] + '/' + fileLineRegexSplit[5]
    minedDate = fileLineRegexSplit[1] + '/' + fileLineRegexSplit[3] + '/' + fileLineRegexSplit[5]
    minedHour = fileLineRegexSplit[7]
    minedAmount = float(fileLineRegexSplit[9])
    
    if minedMonthYear not in byMonth:
        obj = {"total": minedAmount, "transactions": int(1), "blockMin": minedAmount, "blockMax": minedAmount, "usdEndMonth": float(0), "bgnEndMonth": float(0), "usdEquivalentToday": float(0), "bgnEquivalentToday": float(0)}
        obj["usdEndMonth"] = prices[minedMonthYear] * minedAmount
        obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
        obj["usdEquivalentToday"] = prices[minedMonthYear] * hydraPriceTodayUSD
        obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
        byMonth[minedMonthYear] = obj
        continue
    if minedMonthYear in byMonth:
        obj = byMonth[minedMonthYear];
        obj["total"] = obj["total"] + minedAmount
        obj["transactions"] = obj["transactions"] + 1
        obj["blockMin"] = minedAmount if minedAmount < obj["blockMin"] else obj["blockMin"]
        obj["blockMax"] = minedAmount if minedAmount > obj["blockMax"] else obj["blockMax"]
        obj["usdEndMonth"] = obj["total"] * prices[minedMonthYear]
        obj["bgnEndMonth"] = obj["usdEndMonth"] * usdToBGNRate
        obj["usdEquivalentToday"] = obj["total"] * hydraPriceTodayUSD
        obj["bgnEquivalentToday"] = obj["usdEquivalentToday"] * usdToBGNRate
        byMonth[minedMonthYear] = obj
    
print('Statistics by month:')
print(json.dumps(byMonth, indent = 4))

totalMined = float(0)
totalTransactions = int(0)

for byMonthStatistic in byMonth:
    
    totalMined += byMonth[byMonthStatistic]["total"]
    totalTransactions += byMonth[byMonthStatistic]["transactions"]

print("")
print("Statistics overall:")
print("Mined: " + str(totalMined))
print("Transactions: " + str(totalTransactions))
print("USD Equivalent Today:" + str((totalMined * hydraPriceTodayUSD)))
print("BGN Equivalent Today:" + str((totalMined * hydraPriceTodayUSD) * usdToBGNRate))

file.close()