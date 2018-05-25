from flask import Blueprint, render_template, flash, redirect, url_for
from flask_bootstrap import __version__ as FLASK_BOOTSTRAP_VERSION
from flask_nav.elements import Navbar, View, Subgroup, Link, Text, Separator
from markupsafe import escape
from flask_restful import reqparse

from .database import *
from .plot import *
from .forms import SignupForm
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


@frontend.route("/admin/country", methods = ['GET'])
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


@frontend.route("/admin/region",methods = ['GET'])
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




@frontend.route("/admin/plotting/<country>", methods=['GET'])
def plotting(country):
    try:
        country = (country[0].upper()+country[1:]).replace('_',' ')
        dic = fetch_country_data(country)
        p = plot_country(country, dic)
        script, div = components(p)
        return render_template("result.html", script = script, div = div,name=country)
    except:
        return render_template("404notfound.html")

@frontend.route("/admin/plotting_region/<region>", methods=['GET'])
def plotting_region(region):
    try:
        region = (region[0].upper()+region[1:]).replace('_', ' ')
        data = fetch_region_data(region)
        p = plot_region(data)
        script,div = components(p)
        return render_template("result.html", script=script, div=div, name=region)
    except:
        return render_template("404notfound.html")

@frontend.route('/about_us')
def about_us():
    return render_template('about_us.html')


@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/admin/search', methods=['POST'])
def search():
    parser = reqparse.RequestParser()
    parser.add_argument('search', type=str)
    args = parser.parse_args()
    search_country = args.get("search")
    print(search_country)

