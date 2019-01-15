import json
from pprint import pprint

with open('GRILLPLATZOGD.json') as f:
    data = json.load(f)

for item in data['features']:
    print(item)
    break
