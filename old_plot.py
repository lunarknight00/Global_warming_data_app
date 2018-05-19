from flask import Flask,jsonify,request
from .database import *
import json
import pandas as pd
import bokeh

from requests import get
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import inferno
from bokeh.embed import components

# api like data fetch func, not sure is working 
def get_country_data(name):
    connect(host='mongodb://admin:admin@ds215370.mlab.com:15370/ass_3')
    connect('region')
    for e in Region.objects:
        country = e.to_json()
        country = json.loads(country)
        for country_name in country['country_in_region']:
            if country_name['_id'].lower() == name.lower():
                return jsonify(country)

# use requests to fecth sigle country data,input value is country
def fetch_country_data(name):
    url = 'http://127.0.0.1:5000/admin/country'
    # name is the courntry name user input in the webpage
    query = {'country_name':name}
    response = get(url,params=query)
    return response.json()

# use requests ,input value is region
def fetch_region_data(name):
    url = 'http://127.0.0.1:5000/admin/region'
    region = 'East Asia & Pacific'
    query = {'region_name':name}
    response = get(url,params=query)
    return response.json()


# helper function

# preprocess the json dictionary
# input a counntry name and a json dict
# output a tuple country name and a panadas data frame
def country_preprocess(country,dic):
    first_keys = [i for i in dic.keys()]
    for k in dic[first_keys[1]]:
        if k['_id'] == country:
            data = k['statistic']
    return (country,CO2_year(pd.DataFrame(data)))

# co2 line pandas datetime change preprocess
# output a two column data frame

def CO2_year(df):
    processed = df.iloc[:,1:3]
    processed['_id'] = pd.to_datetime(processed['_id'])
    print(processed)
    return processed



### plot line change of one country

def plot_country(country,dic):
    name,processed = country_preprocess(country,dic)
    p = figure(plot_width=1000, plot_height=600, x_axis_type="datetime",y_range = (0,10000))
    p.line(processed['_id'], processed['co2_emission'], color='navy', alpha=0.5,name=country)
    return p


### plot multiplr lines in a region

# helper function

def _country_preprocess(statistics,country):
    data = CO2_year(pd.DataFrame(statistics,columns = ['GDP','_id','co2_emission']))
    data.columns = ['year',country]
    return data
    

def region_preprocess(data,region):
    result = list()
    first_keys = [i for i in data.keys()]
    for d in data[first_keys[1]]:
        result.append(_country_preprocess(d['statistic'],d['_id']))
    return result


# @app.route("/admin/plot",methods = ['GET'])
def plot_region(data,region):
    nums = len(region_preprocess(data,region))
    processed = region_preprocess(data,region)
    countries = [processed[i].columns[1] for i in range(nums)]
    date_column = processed[0]['year']
    co2 = [processed[i][processed[i].columns[1]] for i in range(nums)]
    
    #initialize the figure
    numlines=len(co2)
    mypalette=inferno(numlines)
    
    p = figure(plot_width=1200, plot_height=600,x_axis_type="datetime",title="CO2 emissions")

    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Co2 emissions'

    for i in range(len(countries)):
        p.line(date_column,co2[i],color=mypalette[i],legend = countries[i])
    p.legend.location = "top_left"
    return p

# return one country statistics as chart

def co2_stat(country,dic):
    name,processed = country_preprocess(country,dic)
    processed.columns = ['year',name]
    return processed.describe()


'''
implement example
# Index page
@app.route('/')
def index():
	# Determine the selected feature
	current_feature_name = request.args.get("feature_name")
	if current_feature_name == None:
		current_feature_name = "Sepal Length"
	# Create the plot
	plot = create_figure(current_feature_name, 10)
		
	# Embed plot into HTML via Flask Render
	script, div = components(plot)
	return render_template("iris_index1.html", script=script, div=div,
		feature_names=feature_names,  current_feature_name=current_feature_name)
<html>
<head>
<link
    href="http://cdn.pydata.org/bokeh/release/bokeh-0.12.5.min.css"
    rel="stylesheet" type="text/css">
<link
    href="http://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.5.min.css"
    rel="stylesheet" type="text/css">
<script src="http://cdn.pydata.org/bokeh/release/bokeh-0.12.5.min.js"></script>
<script src="http://cdn.pydata.org/bokeh/release/bokeh-widgets-0.12.5.min.js"></script>
</head>
<body>
<H1>Iris Histogram</H1>
<form action="/">
<select name="feature_name">
	{% for feature in feature_names %}
		{% if feature == current_feature_name %}
			<option selected value="{{ feature }}">{{ feature }}</option> 
		{% else %} 
			<option value="{{ feature }}">{{ feature }}</option> 
		{% endif %}
	{% endfor %}
</select>
<input type="submit">
</form>
{{ script|safe }}
{{ div|safe }}
</body>
</html>
'''