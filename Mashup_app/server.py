from flask import jsonify,request
from mashup_app.database import *
import json
from mashup_app import create_app,database




app = create_app()

@app.route("/admin/delete/country",methods=['DELETE'])
def delete_country():
    name = request.args.get('country_name')
    connect('region')
    for e in Region.objects:
        for a in e.country_in_region:
            if a.name.lower() == name.lower():
                e.country_in_region.remove(a)
                Region(e.name,e.country_in_region).save()
                return jsonify('delete sucessfully'),200
    return jsonify('no such data in database'),404


@app.route("/admin/delete/region",methods=['DELETE'])
def delete_region():
    name = request.args.get('region_name')
    connect('region')
    for e in Region.objects:
        if e.name.lower() == name.lower():
            e.delete()
            return jsonify('delete sucessfully'),200
    return jsonify('no such data in database'),404


@app.route("/admin/post",methods=['POST'])
def post_country():
    country = request.args.get('country_name')
    region = request.args.get('region_name')
    year = request.args.get('year')
    CO2 = request.args.get('CO2')
    GDP = request.args.get('GDP')
    connect('region')
    for re in Region.objects:
        if region.lower() == re.name.lower():
            for coun in re.country_in_region:
                if country.lower() == coun.name.lower():
                    for ye in coun.statistic:
                        if year == ye.year:
                            ye.co2_emission =CO2
                            ye.GDP = GDP
                            Region(re.name,re.country_in_region).save()
                            return jsonify('post sucessfully'),200
                    coun.statistic.append(Year(year,CO2,GDP))
                    Region(re.name, re.country_in_region).save()
                    return jsonify('post sucessfully'), 200
    return jsonify('Wrong input'),404



@app.route("/admin/refresh",methods =['PUT'])
def refresh():
    upload()
    return jsonify('Finished'),200



@app.route("/admin/country", methods = ['GET'])
def get_region():
    name = request.args.get('country_name')
    connect('region')
    if name:
        for e in Region.objects:
            country = e.to_json()
            country = json.loads(country)
            for country_name in country['country_in_region']:
                if country_name['_id'].lower() == name.lower():
                    return jsonify(country),200
        return jsonify('no such data in database'),404





@app.route("/admin/region",methods = ['GET'])
def get_name():
    name = request.args.get('region_name')
    connect('region')
    if name:
        for l in Region.objects:
            if name.lower() == l.name.lower():
                a = l.to_json()
                e = json.loads(a)
                return jsonify(e), 200
        return jsonify('no such data in the database'),404





if __name__ == '__main__':
    database.connect(host='mongodb://admin:admin@ds215370.mlab.com:15370/ass_3')
    app.run(debug=True)
