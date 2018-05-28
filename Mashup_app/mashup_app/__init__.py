from flask import Flask
from flask_bootstrap import Bootstrap
from flask_debug import Debug
from .frontend import frontend
from .nav import nav


def create_app():
    app = Flask(__name__)
    Bootstrap(app)
    Debug(app)
    app.register_blueprint(frontend)
    app.config['BOOTSTRAP_SERVE_LOCAL'] = True
    nav.init_app(app)
    return app
