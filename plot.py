from flask import Flask,jsonify,request
from database import *
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
        if k['_id'].lower() == country.lower():
            data = k['statistic']
    return (country,pd.DataFrame(data,columns = ['GDP','_id','co2_emission']))

# co2 line pandas datetime change preprocess
# output a two column data frame

def CO2_year(df):
    processed = df.iloc[:,1:3]
    processed['_id'] = pd.to_datetime(processed['_id'])
    return processed

# find max y range of the plot
def find_y_max_range(df)
	number = round(float(max(df['co2_emission'])))
	count = 0
	while number != 0:
		number = number // 10
		count += 1  

	number // (10 ** (count -1) )
	if count > 1:
		max_y_range = (number // (10 ** (count-1) ) +1 ) * (10 ** 5)
	else:
		max_y_range = 1
	return max_y_range

### plot line change of one country

def plot_country(country,dic):
    name,processed = country_preprocess(country,dic)
	processed = CO2_year(processed)
    p = figure(plot_width=800,y_range = (0,find_y_max_range(processed)),plot_height=250, x_axis_type="datetime")
    p.line(processed['_id'], processed['co2_emission'],line_width = 4,color='navy', alpha=0.5,name=country)
    return p


### plot multiplr lines in a region

# helper function

def country_preprocess(statistics,country):
    data = CO2_year(pd.DataFrame(statistics,columns = ['GDP','_id','co2_emission']))
    data.columns = ['year',country]
    return data
    

def region_preprocess(data,region):
    result = list()
    first_keys = [i for i in data.keys()]
    for d in data[first_keys[1]]:
        result.append(country_preprocess(d['statistic'],d['_id']))
    return result

def plot_region(data,region):
    nums = len(region_preprocess(data,region))
    processed = region_preprocess(data,region)
    countries = [processed[i].columns[1] for i in range(nums)]
    date_column = processed[0]['year']
    co2 = [processed[i][processed[i].columns[1]] for i in range(nums)]
    range_y = max(find_y_max_range(co2[i]) for i in range(nums))
    #initialize the figure
    numlines=len(co2)
    mypalette=inferno(numlines)
    p = figure(plot_width=1200, plot_height=600,y_range = (0,range_y),x_axis_type="datetime",title="CO2 emissions")
    p.grid.grid_line_alpha=0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Co2 emissions'
    for i in range(len(countries)):
        p.line(date_column,co2[i],color=mypalette[i],legend = countries[i])
    p.legend.location = "top_left"
    return p

# return one country statistics as chart
def statistics_table(country,dic):
    name,processed = country_preprocess(country,dic)
	processed.columns = ['GDP','year','Co2 emission']
	d1 = processed['GDP']
	d2 = processed['Co2 emission']
	result = pd.concat([d1,d2],axis=1, join_axes=[d1.index])
	result = result.apply(pd.to_numeric, errors='ignore')
	result.describe() 
    return processed.describe().to_html()

def _preprocess_multi_lines_statics(list_df):
    return [i.iloc[:,1] for i in list_df]

def multi_statistics_table(data,region):
	processed = _preprocess_multi_lines_statics(region_preprocess(data,region))
	result = pd.concat(processed,axis=1, join_axes=[d1.index])
	result = result.apply(pd.to_numeric, errors='ignore')
	return result.describe().to_html()
	 
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
    
