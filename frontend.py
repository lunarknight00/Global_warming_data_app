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
        Link('Our GitHub', 'https://-----'),
        Separator(),
        Text('Libo Zhuo'),
        Link('Facebook', 'http://----'),
        Separator(),
        Text('Charles Xiao'),
        Link('Facebook', 'http://----'),
        Separator(),
        Text('Yun Lu'),
        Link('Facebook', 'http://----'))))


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
    connect('region')
    if name:
        for l in Region.objects:
            if name.lower() == l.name.lower():
                a = l.to_json()
                e = json.loads(a)
                return jsonify(e), 200
        return jsonify('no such data in the database'),404


@frontend.route("/admin/plot", methods=['GET'])
def plot_region(data, region):
    nums = len(region_preprocess(data, region))
    processed = region_preprocess(data, region)
    countries = [processed[i].columns[1] for i in range(nums)]
    date_column = processed[0]['year']
    co2 = [processed[i][processed[i].columns[1]] for i in range(nums)]

    # initialize the figure
    numlines = len(co2)
    mypalette = inferno(numlines)

    p = figure(plot_width=1200, plot_height=600, x_axis_type="datetime", title="CO2 emissions")

    p.grid.grid_line_alpha = 0.3
    p.xaxis.axis_label = 'Date'
    p.yaxis.axis_label = 'Co2 emissions'

    for i in range(len(countries)):
        p.line(date_column, co2[i], color=mypalette[i], legend=countries[i])
    p.legend.location = "top_left"
    return p

@frontend.route("/admin/plotting/<country>", methods=['GET'])
def plotting(country):
    dic = fetch_country_data(country)
    p = plot_country(country, dic)
    script, div = components(p)
    return render_template("result.html", script = script, div = div)

@frontend.route('/about_us')
def about_us():
    return render_template('about_us.html')


@frontend.route('/')
def index():
    return render_template('index.html')

@frontend.route('/admin/search', methods=['POST'])
def search():
    print('here')
    parser = reqparse.RequestParser()
    parser.add_argument('search', type=str)
    args = parser.parse_args()
    search_country = args.get("search")
    print(search_country)

# Shows a long signup form, demonstrating form rendering.
@frontend.route('/example-form/', methods=('GET', 'POST'))
def example_form():
    form = SignupForm()

    if form.validate_on_submit():
        # We don't have anything fancy in our application, so we are just
        # flashing a message when a user completes the form successfully.
        #
        # Note that the default flashed messages rendering allows HTML, so
        # we need to escape things if we input user values:
        flash('Hello, {}. You have successfully signed up'
              .format(escape(form.name.data)))

        # In a real application, you may wish to avoid this tedious redirect.
        return redirect(url_for('.index'))

    return render_template('signup.html', form=form)
