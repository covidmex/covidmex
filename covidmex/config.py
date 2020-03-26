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
    # SQLAlchemy + PostgreSQL
    MYSQL_USER = os.getenv('MYSQL_USER','')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD','')
    MYSQL_HOST = os.getenv('MYSQL_HOST')
    MYSQL_DB = os.getenv('MYSQL_DB')
    MYSQL_ECHO = False
    SQLALCHEMY_DATABASE_URI = "mysql://{0}:{1}@{2}/{3}".format(MYSQL_USER, MYSQL_PASSWORD, MYSQL_HOST, MYSQL_DB)
    SQLALCHEMY_POOL_SIZE = 20
    SQLALCHEMY_TRACK_MODIFICATIONS = False