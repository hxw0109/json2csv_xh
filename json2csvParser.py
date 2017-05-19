import json
import pprint
from functools import reduce
import operator
import csv
from datetime import datetime
import pandas, glob, xlwt, os

fp = open('vehiclemonitoringalpha-export.json', 'r')
rawData = json.load(fp)
pprint.pprint(rawData, depth=1)

def getDataFromJson (data, mapList):
    return reduce(operator.getitem, mapList, data)

vehicleList = ["AVL Vehicle 2", "Ford HiL", "Talus' Car", "X's Car"]
timeRefPython = datetime(1970,1,1,0,0,0)
timeRefSwift = datetime(2001,1,1,0,0,0)
deltaT_in_seconds = (timeRefSwift-timeRefPython).total_seconds()

# Get activity and usage data
for vehicle in vehicleList:
    activityData = getDataFromJson(rawData, ["activities", vehicle])
    csvFilename = "activity " + vehicle + ".csv"
    csvFileheader = ["key","category","description","duration","durationInVehicle","location","timestamp","userID","username","date"]
    with open(csvFilename,'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFileheader)
        writer.writeheader()
        for key in activityData:
            activityData[key]["key"] = key
            timestamp = activityData[key]["timestamp"] + deltaT_in_seconds
            activityData[key]["date"] = str(datetime.fromtimestamp(timestamp))
            writer.writerow(activityData[key])

    usageData = getDataFromJson(rawData, ["usages", vehicle])
    csvFilename = "usage " + vehicle + ".csv"
    csvFileheader = ["key","timestamp","usageBool","userID","username","date"]
    with open(csvFilename,'w',newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFileheader)
        writer.writeheader()
        for key in usageData:
            usageData[key]["key"] = key
            timestamp = usageData[key]["timestamp"] + deltaT_in_seconds
            usageData[key]["date"] = str(datetime.fromtimestamp(timestamp))
            writer.writerow(usageData[key])

    eventData = getDataFromJson(rawData, ["events", vehicle])
    csvFilename = "event " + vehicle + ".csv"
    csvFileheader = ["key","duration","durationInVehicle","event","isInRange","timestamp","userID","username","date"]
    with open(csvFilename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csvFileheader)
        writer.writeheader()
        for key in eventData:
            eventData[key]["key"] = key
            timestamp = eventData[key]["timestamp"] + deltaT_in_seconds
            eventData[key]["date"] = str(datetime.fromtimestamp(timestamp))
            writer.writerow(eventData[key])

# Write file to excel format
wb = xlwt.Workbook()
for filename in glob.glob("/Users/admin/Desktop/Python/json2csv_xh/*.csv"):
    (f_path, f_name) = os.path.split(filename)
    (f_short_name, f_extension) = os.path.splitext(f_name)
    ws = wb.add_sheet(f_short_name)
    spamReader = csv.reader(open(filename, 'r'))
    for rowx, row in enumerate(spamReader):
        for colx, value in enumerate(row):
            ws.write(rowx, colx, value)
wb.save("/Users/admin/Desktop/Python/json2csv_xh/summary.xls")