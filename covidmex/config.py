# -*- coding: utf-8 -*-

import os
from datetime import timedelta


class BaseConfig(object):
    PROJECT = "covidmex"
    # Get app root path, also can use flask.root_path.
    # ../../config.py
    PROJECT_ROOT = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    DEBUG = True
    TESTING = False
    ADMINS = ['guillermoalvarado89@gmail.com']
    # http://flask.pocoo.org/docs/quickstart/#sessions
    SECRET_KEY = 'secret key'

class DefaultConfig(BaseConfig):
    DEBUG = True
    # FLask admin
    COVIDMEX_ADMIN_PASSWORD = os.getenv('COVIDMEX_ADMIN_PASSWORD','')
    COVIDMEX_ADMIN_USER = os.getenv('COVIDMEX_ADMIN_USER','')
    # SQLAlchemy + PostgreSQL
    MYSQL_USER = os.getenv('MYSQL_USER','')
    MYSQL_ROOT_PASSWORD = os.getenv('MYSQL_ROOT_PASSWORD','')
    MYSQL_HOSTNAME = os.getenv('MYSQL_HOSTNAME')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}?auth_plugin=mysql_native_password".format(MYSQL_USER, MYSQL_ROOT_PASSWORD, MYSQL_HOSTNAME, MYSQL_DB)
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False
