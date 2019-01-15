from flask import Flask
from flask import render_template
import json
from grill_place import place
app = Flask(__name__)

datamap = []

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/store',methods=['POST'])
def store_data(json_data):
        data = json.load(json_data)
        grill_instance = place()

        #check if data has all the fields to be a grillplace
        if 'geometry' in data and 'id' in data and 'properties' in data:
            grill_instance.id = data['id']
            grill_instance.geometry = data['geometry']
            grill_instance.properties = data['properties']

            datamap.append(grill_instance)
            return "added to the dataset"
        else:
            return "malformed dataa couldn't be added"

@app.route('/grills')
def display_grill_spots():
    return render_template('grillspots.html',datamap)


if __name__ == '__main__':
    app.run()
