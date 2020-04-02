# -*- coding: utf-8 -*-

import os, sys
import locale

from flask import Flask, Response
from flask_admin import Admin
from flask_basicauth import BasicAuth
from werkzeug.exceptions import HTTPException

from config import DefaultConfig
from extensions import db
from models import State, Case, CountryProcedence, Totals
from utils import INSTANCE_FOLDER_PATH
from views_blueprint import views_blueprint
from import_controller import import_api


# For import *
__all__ = ['create_app']



def create_app(config=None, app_name=None, blueprints=None):
    """Create a Flask app."""
    if app_name is None:
        app_name = DefaultConfig.PROJECT

    if os.environ.get('COVIDMEX_ENVIRONMENT') == 'production':
        from .production_config import ProductionConfig
        config = ProductionConfig

    app = Flask(
        app_name,
        instance_relative_config=True,
        static_url_path='', 
        static_folder='static',
        template_folder='templates',
        instance_path=INSTANCE_FOLDER_PATH,
    )
        # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    configure_app(app, config)
    configure_extensions(app)
    sys.path.append(os.path.join(os.path.dirname(__file__), "covidmex"))

    if os.environ.get('COVID_ENVIRONMENT') == 'production':
        # sentry.init_app(app)
        pass

    return app

def configure_app(app, config=None):
    """Different ways of configurations."""
    # http://flask.pocoo.org/docs/api/#configuration
    app.config.from_object(DefaultConfig)
    if config:
        app.config.from_object(config)
    #locale.setlocale(locale.LC_TIME, 'es_ES')




    app.register_blueprint(views_blueprint)
    app.register_blueprint(import_api, url_prefix="/api/v1")

def configure_extensions(app):
    from flask_admin.contrib.sqla import ModelView
    # flask-sqlalchemy
    db.init_app(app)
    # flask-admin
    app.config['FLASK_ADMIN_SWATCH'] = 'yeti'



    class AuthException(HTTPException):
        def __init__(self, message):
            super(AuthException, self).__init__(message, Response(
                message, 401,
                {'WWW-Authenticate': 'Basic realm="Login Required"'}
            ))



    # overwrite ModelView of flask_admin to just affects admin page
    class ModelView(ModelView):
        def is_accessible(self):
            if not basic_auth.authenticate():
                raise AuthException('Not authenticated. Refresh the page.')
            else:
                return True

        def inaccessible_callback(self, name, **kwargs):
            return redirect(basic_auth.challenge())


    app.config['BASIC_AUTH_USERNAME'] = app.config['COVIDMEX_ADMIN_USER']
    app.config['BASIC_AUTH_PASSWORD'] = app.config['COVIDMEX_ADMIN_PASSWORD']
    basic_auth = BasicAuth(app)
    admin = Admin(app, url='/superuser', name='covidmex', template_mode='bootstrap3')
    admin.add_view(ModelView(Case, db.session))
    admin.add_view(ModelView(CountryProcedence, db.session))
    admin.add_view(ModelView(State, db.session))
    admin.add_view(ModelView(Totals, db.session))
