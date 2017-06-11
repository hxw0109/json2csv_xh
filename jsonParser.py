import json, pprint, operator, datetime
from functools import reduce
from datetime import datetime

fp = open('vehiclemonitoringalpha-export.json', 'r')
rawData = json.load(fp)
# pprint.pprint(rawData, depth=2)


# Function to get list data
def getDataFromJson (data, mapList):
    return reduce(operator.getitem, mapList, data)

# Reference time difference between python and swift
timeRefPython = datetime(1970,1,1,0,0,0)
timeRefSwift = datetime(2001,1,1,0,0,0)
deltaT_in_seconds = (timeRefSwift-timeRefPython).total_seconds()

# Vehicle list
vehicleList = ["AVL Vehicle 2", "Ford HiL", "Talus' Car", "X's Car"]

# Get data associated to "vehicle"
vehicleDuration = []
vehicleUsage = []
vehicleDataRaw = getDataFromJson(rawData, ["vehicle"])
for vehicle in vehicleDataRaw:
    duration = vehicleDataRaw[vehicle]['duration']/3600 # in hours
    usage = vehicleDataRaw[vehicle]['durationInVehicle']/3600 # in hours
    vehicleDuration.append(duration)
    vehicleUsage.append(usage)

# Get data associated to "activities"
activityDataRaw = getDataFromJson(rawData, ["activities"])
activities = {}
for vehicle in activityDataRaw:
    activities[vehicle] = {'category':[] , 'duration':[], 'durationInVehicle':[], 'username':[]}
    for item in activityDataRaw[vehicle]:
        activities[vehicle]['category'].append(activityDataRaw[vehicle][item]['category'])
        activities[vehicle]['duration'].append(activityDataRaw[vehicle][item]['duration']/60) # in minutes
        activities[vehicle]['durationInVehicle'].append(activityDataRaw[vehicle][item]['durationInVehicle']/60) # in minutes
        activities[vehicle]['username'].append(activityDataRaw[vehicle][item]['username'])


# Get data associated to "usages"
usageDataRaw = getDataFromJson(rawData,['usages'])
usages = {}
for vehicle in usageDataRaw:
    usages[vehicle] = {'timestamp':[], 'usageBool':[]}




import plotly.plotly as py
import plotly.graph_objs as go
trace1 = go.Bar(
            x = vehicleList,
            y = vehicleDuration,
            name = 'Total time'
    )
trace2 = go.Bar(
            x = vehicleList,
            y = vehicleUsage,
            name = 'Time in vehicle'
    )
data = [trace1, trace2]
layout = go.Layout(
        title = 'Vehicle Usage',
        xaxis = dict(
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
        yaxis = dict(
            title='Usage in hours',
            titlefont=dict(
                size=16,
                color='rgb(107, 107, 107)'
            ),
            tickfont=dict(
                size=14,
                color='rgb(107, 107, 107)'
            )
        ),
    barmode='group'
    )
fig = go.Figure(data=data, layout=layout)
py.plot(fig, filename='usage-bar')