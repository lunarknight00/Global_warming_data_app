from flask import Flask,jsonify,request
from .database import *
from .frontend import *
import json
import pandas as pd
import bokeh

from requests import get
from bokeh.plotting import figure, output_file, show
from bokeh.palettes import inferno
from bokeh.embed import components


# use requests to fecth sigle country data,input value is country
def fetch_country_data(name):
	url = 'http://127.0.0.1:5000/admin/country'
	query = {'country_name':name}
	response = get(url,params=query)
	return response.json()

# use requests ,input value is region
def fetch_region_data(name):
	url = 'http://127.0.0.1:5000/admin/region'
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
	return (country,pd.DataFrame(data))

# co2 line pandas datetime change preprocess
# output a two column data frame

def CO2_year(df):
	processed = df.iloc[:,1:3]
	processed['_id'] = pd.to_datetime(processed['_id'])
	return processed

# find max y range of the plot
def find_y_max_range(df):
	number = round(float(max(df['co2_emission'])))
	count = 0
	while number != 0:
		number = number // 10
		count += 1
	if count > 1:
		max_y_range = (number // (10 ** (count-1) ) +1 ) * (10 ** 5)
	else:
		max_y_range = 1
	return max_y_range

### plot line change of one country

def plot_country(country,dic):
	name,processed = country_preprocess(country,dic)
	processed = CO2_year(processed)
	p = figure(plot_width=1200,y_range = (0,find_y_max_range(processed)),plot_height=600, x_axis_type="datetime",title="CO2 emissions")
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Co2 emissions'
	p.line(processed['_id'], processed['co2_emission'],line_width = 4,color='navy', alpha=0.5,name=country)
	return p



### plot multiplr lines in a region

# helper function

def _country_preprocess(statistics,country):
	data = CO2_year(pd.DataFrame(statistics,columns = ['GDP','_id','co2_emission']))
	data.columns = ['year',country]
	return data


def region_preprocess(data):
	result = list()
	first_keys = [i for i in data.keys()]
	for d in data[first_keys[1]]:
		result.append(_country_preprocess(d['statistic'],d['_id']))
	return result


def plot_region(data):
	nums = len(region_preprocess(data))
	processed = region_preprocess(data)
	countries = [processed[i].columns[1] for i in range(nums)]
	date_column = processed[0]['year']
	co2 = [processed[i][processed[i].columns[1]] for i in range(nums)]

	#initialize the figure
	numlines=len(co2)
	mypalette=inferno(numlines)

	p = figure(plot_width=1200, plot_height=600,x_axis_type="datetime",title="CO2 emissions")

	p.grid.grid_line_alpha=0.3
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'region Co2 emissions'

	for i in range(len(countries)):
		p.line(date_column,co2[i],color=mypalette[i],legend = countries[i])
	p.legend.location = "top_left"
	return p

# return one country statistics as chart

def co2_stat(country,dic):
	name,processed = country_preprocess(country,dic)
	processed.columns = ['year',name]
	return processed.describe()

def statistics_table(country,dic):
	name,processed = country_preprocess(country,dic)
	processed.columns = ['GDP','year','Co2 emission']
	d1 = processed['GDP']
	d2 = processed['Co2 emission']
	result = pd.concat([d1,d2],axis=1, join_axes=[d1.index])
	result = result.apply(pd.to_numeric, errors='ignore')
	result.describe()
	return result.describe().T.to_html()

def _preprocess_multi_lines_statics(list_df):
	return [i.iloc[:,1] for i in list_df]


def multi_statistics_table(data):
	processed = _preprocess_multi_lines_statics(region_preprocess(data))
	result = pd.concat(processed,axis=1, join_axes=[processed[0].index])
	result = result.apply(pd.to_numeric, errors='ignore')
	return result.describe().T.to_html()

def multi_GDP_statistics_table(data):
	processed = _preprocess_multi_lines_statics(GDP_region_preprocess(data))
	result = pd.concat(processed,axis=1, join_axes=[processed[0].index])
	result = result.apply(pd.to_numeric, errors='ignore')
	return result.describe()

def scatter_country(country,dic):
	name,processed = country_preprocess(country,dic)
	processed.columns = ['GDP','year','Co2 emission']
	d1 = processed['GDP']
	d2 = processed['Co2 emission']
	p = figure(title = "GDP vs Co2 emmisions")
	p.xaxis.axis_label = 'GDP'
	p.yaxis.axis_label = 'Co2 emmisions'
	p.circle(d1,d2,color = 'red',fill_alpha=0.2, size=10)
	return p

# plot gdp multilines
# helper function

def GDP_year(df):
	d1 = df['_id']
	d2 = df['GDP']
	processed = pd.concat([d1,d2],axis=1, join_axes=[d1.index])
	processed['_id'] = pd.to_datetime(processed['_id'])
	return processed
	

def __country_preprocess(statistics,country):
	data = GDP_year(pd.DataFrame(statistics,columns = ['GDP','_id','co2_emission']))
	data.columns = ['year',country]
	return data
	

def GDP_region_preprocess(data):
	result = list()
	first_keys = [i for i in data.keys()]
	for d in data[first_keys[1]]:
		result.append(__country_preprocess(d['statistic'],d['_id']))
	return result

	

def plot_region_GDP(data):
	nums = len(GDP_region_preprocess(data))
	processed = GDP_region_preprocess(data)
	countries = [processed[i].columns[1] for i in range(nums)]
	date_column = processed[0]['year']
	GDP = [processed[i][processed[i].columns[1]] for i in range(nums)]

	#initialize the figure
	numlines=len(GDP)
	mypalette=inferno(numlines)

	p = figure(plot_width=1200, plot_height=600,x_axis_type="datetime",title="GDP")

	p.grid.grid_line_alpha=0.3
	p.xaxis.axis_label = 'Date'
	p.yaxis.axis_label = 'Region GDP'

	for i in range(len(countries)):
		p.line(date_column,co2[i],color=mypalette[i],legend = countries[i])
	p.legend.location = "top_left"
	return p
