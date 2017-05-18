import json
import pprint
from functools import reduce
import operator
import csv

fp = open('vehiclemonitoringalpha-export.json', 'r')
rawData = json.load(fp)
pprint.pprint(rawData, depth=1)


def getDataFromJson (data, mapList):
    return reduce(operator.getitem, mapList, data)
vehicleList = ["AVL Vehicle 2", "Ford HiL", "Talus' Car", "X's Car"]

# Get activity and usage data

for vehicle in vehicleList:
    activityData = getDataFromJson(rawData, ["activities", vehicle])
    csvFilename = "activity " + vehicle + ".csv"
    csvFileheader = ["category","description","duration","durationInVehicle","location","timestamp","userID","username"]
    with open(csvFilename,'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFileheader)
        writer.writeheader()
        for key in activityData:
            writer.writerow(activityData[key])

    usageData = getDataFromJson(rawData, ["usages", vehicle])
    csvFilename = "usage " + vehicle + ".csv"
    csvFileheader = ["timestamp","usageBool","userID","username"]
    with open(csvFilename,'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFileheader)
        writer.writeheader()
        for key in usageData:
            writer.writerow(usageData[key])
