from flask import Flask
from flask import render_template
from flask import request
import json
from grill_place import *
from collections import Counter
import weather

app = Flask(__name__)

datamap = grill_historics()
@app.route('/')
def index():
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
                stay_times.append(measurement['timestamp'] - find_appear_date(ip,history))

        #assume no messages go missing and we dont need to correct for errors
        tracked = measurement

    if len(stay_times) >1:
        return (sum(stay_times) / len(stay_times)) / 60
    return 0

def find_appear_date(ip_addr,history):
    for m in history:
        if ip_addr in m['ips']:
            return m['timestamp']




@app.route('/analytics/<grill_id>')
def analytics(grill_id):
    grill_data = datamap.get_grill(grill_id)
    history = datamap.get_history(grill_data)
    if not history:
        return "no information about this grillspot available"
    avg_amount_people = 0
    change_people = []

    for measurement in history:
        #figure out average amount of people
        avg_amount_people += measurement['amount']
        change_people.append((measurement['amount']))


    avg_amount_people = avg_amount_people / len(history)
    #normally you would store an api key like this, but i haven't got time to set up config files for all my project partners
    #hardcoding vienna also isn't the prettiest solution, but we can assume all grillspots are in vienna.

    longitude, latitude = grill_data['geometry']['coordinates']
    forecast = weather.format_for_frontend(weather.get_weather_location('0198c8157e5c1dc6c01eec615e31c277',latitude, longitude))
    return render_template('analytics.html', forecast_data= forecast, amount= grill_data['amount'],average =avg_amount_people,stay_time= calc_stay_time(history), group_size = most_common(change_people)[0][0])

@app.route('/grills')
def display_grill_spots():
    data = datamap.get_heads()
    return render_template('grillspots.html',datamap=data)


if __name__ == '__main__':
    app.run()
