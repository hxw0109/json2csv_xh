import json
import pprint
from functools import reduce
import operator

fp = open('vehiclemonitoringalpha-export.json', 'r')

dataDict = json.load(fp)

# pprint.pprint(dataDict, depth=1)

from functools import reduce
import operator

def getFromDict (data, mapList):
    return reduce(operator.getitem, mapList, data)

generatedData = getFromDict(dataDict, ["activities","AVL Vehicle 2"])

# for key, value in generatedData.items():
#     print (key, " value:", value["duration"])

# pprint.pprint(getFromDict(dataDict, ["beacons","beacon1"]))


import csv
with open('example.csv','w',newline='') as csvfile:
    fieldnames = ["category","description","duration","durationInVehicle","location","timestamp","userID","username"]
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for key in generatedData:
        writer.writerow(generatedData[key])


