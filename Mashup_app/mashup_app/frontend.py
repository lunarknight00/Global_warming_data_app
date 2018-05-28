from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape
from flask_restful import reqparse
from .database import *
from .plot import *
from .nav import nav



frontend = Blueprint('frontend', __name__)

# We're adding a navbar as well through flask-navbar. In our example, the
# navbar has an usual amount of Link-Elements, more commonly you will have a
# lot more View instances.
nav.register_element('frontend_top', Navbar(
    View('Home', '.index'),
    Subgroup(
        'About us',
        View('About us', '.about_us'),
        Link('Our GitHub', 'https://github.com/lunarknight00/meshup_app'),
        Separator(),
        Text('Libo Zhuo'),
        Link('Facebook', 'https://www.facebook.com/profile.php?id=100003725844785'),
        Separator(),
        Text('Charles Xiao'),
        Link('Facebook', 'https://www.facebook.com/profile.php?id=100019738470628'),
        Separator(),
        Text('Yun Lu'),
        Link('Facebook', 'https://www.facebook.com/profile.php?id=100003946230232'))))



@frontend.route("/admin/plotting/<country>", methods=['GET'])
def plotting(country):
    try:
        country = (country[0].upper()+country[1:]).replace('_',' ')
        dic = fetch_country_data(country)
        p = plot_country(country, dic)
        table = statistics_table(country, dic)
        script, div = components(p)
        return render_template("result.html", script = script, div = div, name=country, table=table)
    except:
        return render_template("404notfound.html")

@frontend.route("/admin/plotting_region/<region>", methods=['GET'])
def plotting_region(region):
    try:
        region = (region[0].upper()+region[1:]).replace('_', ' ')
        data = fetch_region_data(region)
        table = multi_statistics_table(data)
        p = plot_region(data)
        script,div = components(p)
        scatter_data = plot_region_GDP(data)
        script_1, scatter = components(scatter_data)
        GDP_table = multi_GDP_statistics_table(data)
        return render_template("result.html", script=script, div=div, name=region, table=table, script_1=script_1,
                       div_1=scatter, CO2='CO2',GDP='GDP', table_1 = GDP_table)
    except:
        return render_template("404notfound.html")

@frontend.route('/about_us', methods = ['GET'])
def about_us():
    return render_template('about_us.html')

@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/admin/search/', methods=['POST'])
def search():
    keyword = request.form.get("search")
    try:
        region = keyword
        data = fetch_region_data(region)
        table = multi_statistics_table(data)
        p = plot_region(data)
        script, div = components(p)
        scatter_data = plot_region_GDP(data)
        script_1, scatter = components(scatter_data)
        GDP_table = multi_GDP_statistics_table(data)
        return render_template("result.html", script=script, div=div, name=region, table=table,
                               script_1=script_1, div_1 = scatter,table_1 = GDP_table, CO2='CO2',GDP='GDP')
    except:
        try:
            country = keyword
            dic = fetch_country_data(country)
            p = plot_country(country, dic)
            table = statistics_table(country, dic)
            script, div = components(p)
            return render_template("result.html", script=script, div=div, name=country, table=table)
        except:
            return render_template("404notfound.html"),404




