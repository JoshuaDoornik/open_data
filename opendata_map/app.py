from flask import Flask
from flask import render_template
from flask import request
import json
from grill_place import *
from collections import Counter

app = Flask(__name__)

datamap = grill_historics()
@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/store',methods=['POST'])
def store_data():
        data = request.get_json(silent=False)
        if 'id' in data:
            datamap.append(data)
            return "added json to dataset"
        else:
            return "json was malformed. no id tag found"



def most_common(L):
    counter = Counter()
    for i in L:
        counter[i] +=1
    return counter.most_common(1)

def calc_stay_time(history):
    tracked = set(history[0]['ips'])
    stay_times = []
    for measurement in history:
        measurement = set(measurement['ips'])
        inter = tracked.intersection(measurement)
        if inter:
            ips_left  =tracked - inter
            for ip in ips_left:
                stay_times.append((measurement['timestamp'] - find_appear_date(ip,history)))
        diff = measurement - tracked
        tracked = (tracked - inter).union(diff)

    if len(stay_times) >1:
        return (sum(stay_times) / len(stay_times)) / 60
    return 0

def find_appear_date(ip_addr,history):
    for m in history:
        if ip_addr in m['ips']:
            return m['timestamp']




@app.route('/analytics/<grill_id>')
def analytics(grill_id):
    print(datamap.get_grill(grill_id))
    history = datamap.get_history(datamap.get_grill(grill_id))
    if not history:
        return "no information about this grillspot available"
    avg_amount_people = 0
    avg_stay_time = 0
    meantime = 0
    change_people = []
    prev = history[0]

    for measurement in history:
        #figure out average amount of people
        avg_amount_people += measurement['amount']
        change_people.append((measurement['amount']))


    avg_amount_people = avg_amount_people / len(history)
    print(most_common(change_people))
    return render_template('analytics.html',name=grill_id,amount = avg_amount_people,stay_time= calc_stay_time(history), group_size = most_common(change_people)[0][0])

@app.route('/grills')
def display_grill_spots():
    data = datamap.get_heads()
    return render_template('grillspots.html',datamap=data)


if __name__ == '__main__':
    app.run()
