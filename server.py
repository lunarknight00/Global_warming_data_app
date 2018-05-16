from flask import Flask,jsonify,request
from database import *
import json

app = Flask(__name__)

@app.route("/admin/country", methods = ['GET'])
def get_region():
    name = request.args.get('country_name')
    connect('region')
    if name:
        for e in Region.objects:
            country = e.to_json()
            country = json.loads(country)
            for country_name in country['country_in_region']:
                print(country_name)
                if country_name['_id'].lower() == name.lower():
                    return jsonify(country),200
        return jsonify('no such data in database'),404





@app.route("/admin/region",methods = ['GET'])
def get_name():
    name = request.args.get('region_name')
    print(name)
    connect('region')
    if name:
        for l in Region.objects:
            if name.lower() == l.name.lower():
                a = l.to_json()
                e = json.loads(a)
                return jsonify(e), 200
        return jsonify('no such data in the database'),404





if __name__ == '__main__':
    connect(host='mongodb://admin:admin@ds215370.mlab.com:15370/ass_3')
    app.run()
