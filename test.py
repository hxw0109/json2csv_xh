import json
import pprint

fp = open('vehiclemonitoringalpha-export.json', 'r')
data = json.load(fp)
pprint.pprint(data, depth=2)