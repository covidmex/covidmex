# -*- coding: utf-8 -*-

import os, sys

from flask import Flask
#from .models import User as UserModel, Role, Account
from .config import DefaultConfig
from .extensions import db
from .utils import INSTANCE_FOLDER_PATH
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

    app.register_blueprint(views_blueprint)
    app.register_blueprint(import_api, url_prefix="/api/v1")

def configure_extensions(app):
    # flask-sqlalchemy
    db.init_app(app)