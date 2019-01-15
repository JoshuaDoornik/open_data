from flask import Flask
from flask import render_template
from flask import request
import json
from grill_place import place
app = Flask(__name__)

datamap = []

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/store',methods=['POST'])
def store_data():
        data = request.get_json(silent=False)
        grill_instance = place()

        #check if data has all the fields to be a grillplace
        if 'geometry' in data and 'id' in data and 'properties' in data:
            grill_instance.id = data['id']
            grill_instance.geometry = data['geometry']
            grill_instance.properties = data['properties']
            grill_instance.place =grill_instance.properties['LAGE']
            grill_instance.n_people = data['amount']
        else:
            return "malformed dataset"
        add_grillplace(grill_instance)
        return "added to dataset"

def add_grillplace(grillplace: place):
    if grillplace not in datamap:
        datamap.append(grillplace)

@app.route('/grills')
def display_grill_spots():
    print(datamap)
    return render_template('grillspots.html',datamap=datamap)


if __name__ == '__main__':
    app.run()
