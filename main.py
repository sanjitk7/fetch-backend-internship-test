import csv
import time
import sys

payerAccounts = []
balance = int(sys.argv[1])
with open("./transactions.csv", 'r') as file:
  transactions = csv.reader(file)
  next(transactions)
  for transaction in transactions:
      payerAccounts.append({"payer":transaction[0],"points":int(transaction[1]),"timestamp":transaction[2]})

payerAccounts.sort(key=lambda x:time.mktime(time.strptime(x['timestamp'], '%Y-%m-%dT%H:%M:%SZ')))

# the condition no points can go negative takes precedence because new points are added (negative payer points are points received by user)
# this would increase user points and affect the other condition of older payer accounts being chosen.

# split all the negative values and positive values of payer points
neg_acc = []
pos_acc = []
for acc in payerAccounts:
  if acc["points"] >= 0:
    pos_acc.append(acc)
  else:
    neg_acc.append(acc)

# add -ve points into user account and then use the user points for +ve points in payer accounts

for acc in neg_acc:
  balance -= acc["points"]

# use balance against +ve payer accounts
res = {}
for acc in pos_acc:
  if acc["points"] < balance:
    balance -= acc["points"]
    res[acc["payer"]] = 0
  else:
    acc["points"] -= balance
    balance = 0
    res[acc["payer"]] = acc["points"]

print(res)
    