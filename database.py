###COMP9321 Assignment 3--Database Part
###Author Yitong Xiao
import csv
import os
from mongoengine import connect,StringField, Document,FloatField,ListField,EmbeddedDocument,EmbeddedDocumentField


class Year(EmbeddedDocument):
    year = StringField(required = True, primary_key=True)
    co2_emission = StringField()
    GDP = StringField()
    def __init__(self,year,co2_emission,GDP,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.year = year
        self.co2_emission = co2_emission
        self.GDP = GDP


class Country(EmbeddedDocument):
    name = StringField(required = True, primary_key=True)
    type = StringField()
    statistic =ListField(EmbeddedDocumentField(Year))
    def __init__(self,name,type,statistic,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.type = type
        self.statistic = statistic


class Region(Document):
    name =StringField(required = True, primary_key=True)
    country_in_region = ListField(EmbeddedDocumentField(Country))
    def __init__(self,name,country_in_region,*args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.country_in_region =country_in_region

directory_GDP ='D:/9321/9321ass_3/GDP'
directory_CO2 ='D:/9321/9321ass_3/CO2'
directory_HDI ='D:/9321/9321ass_3/HDI'
final_GDP = {}
final_CO2 ={}
final_HDI ={}
for filename in os.listdir(directory_GDP):
    if not filename.endswith('csv'):
        continue
    csvFile = open(f'GDP/{filename}','r')
    reader = csv.reader(csvFile)
    result ={}
    year =[]
    for line in reader:
        if line[0] =='Data from database: World Development Indicators':
            break
        if line[1] == 'Series Code':
            for i in range(4,len(line)):
                year.append(line[i][:4])
            continue
        year_GDP ={}
        for i in range(len(line)-4):
            if not line[i+4] or line[i+4] =='..':
                year_GDP[year[i]] = 'No data'
            else:
                year_GDP[year[i]] = line[i+4]
        result[line[2]] =year_GDP
    final_GDP[filename[:-4]] = result
    csvFile.close()
for filename in os.listdir(directory_CO2):
    if not filename.endswith('csv'):
        continue
    csvFile = open(f'CO2/{filename}', 'r')
    reader = csv.reader(csvFile)
    result = {}
    year = []
    for line in reader:
        if line[0] =='Data from database: World Development Indicators':
            break
        if line[1] =='Country Code':
            for i in range(4,len(line)-3):
                year.append(line[i][:4])
            continue
        year_CO2 = {}
        for i in range(len(line)-7):
            if not line[i+4] or line[i+4] =='..':
                year_CO2[year[i]] = 'No data'
            else:
                year_CO2[year[i]] = line[i+4]
        result[line[0]] = year_CO2
    final_CO2 = result
    csvFile.close()
for filename in os.listdir(directory_HDI):
    if not filename.endswith('csv'):
        continue
    csvFile = open(f'HDI/{filename}','r')
    reader = csv.reader(csvFile)
    for line in reader:
        if line[1] == 'Country':
            continue
        if float(line[2]) >= 0.9:
            final_HDI[line[1]] = 'Developed'
        else:
            final_HDI[line[1]] ='Developing'
    csvFile.close()

connect(host = 'mongodb://admin:admin@ds215370.mlab.com:15370/ass_3')
for region in final_GDP:
    region_pro = []
    for country in final_GDP[region]:
        year_pro = []
        for year in final_GDP[region][country]:
            if country in final_CO2:
                year_pro.append(Year(year, final_GDP[region][country][year],final_CO2[country][year]))
            else:
                year_pro.append(Year(year, final_GDP[region][country][year], 'No data'))
        if country in final_HDI:
            region_pro.append(Country(country,final_HDI[country],year_pro))
        else:
            region_pro.append(Country(country, 'No type for this country', year_pro))

    result = Region(region,region_pro)
    connect('region')
    result.save()

