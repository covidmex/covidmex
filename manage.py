# -*- coding: utf-8 -*-

import os
from datetime import datetime, timedelta
import urllib

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import database_exists, create_database, drop_database

from covidmex import create_app
from covidmex.extensions import db
from covidmex.models import State, CountryProcedence, Case
from covidmex.config import DefaultConfig
from covidmex.import_controller import datos

app = create_app()
configuration = DefaultConfig

if os.environ.get('COVIDMEX_ENVIRONMENT') and os.environ.get('COVIDMEX_ENVIRONMENT') == 'production':
    from covidmex.production_config import ProductionConfig
    configuration = ProductionConfig
    
app.config['SQLALCHEMY_DATABASE_URI'] = configuration.SQLALCHEMY_DATABASE_URI
#app.config['SERVER_NAME'] = 'api.sentinel.la'

manager = Manager(app)
migrate = Migrate(app, db)
manager.add_command('db', MigrateCommand)

@manager.command
def run():
    """Run in local machine."""
    context = ('certificates/ssl-bundle-sentinella.crt', 'certificates/STAR_sentinel_la.key')
    if os.environ.get('COVIDMEX_ENVIRONMENT') == 'production':
        app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=context)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)

@manager.command
def initdb():
    """Destroys and creates the database + tables."""
    DB_URL = app.config.get('SQLALCHEMY_DATABASE_URI')
    if database_exists(DB_URL):
        print('Deleting database.')
        drop_database(DB_URL)
    if not database_exists(DB_URL):
        print('Creating database.')
        create_database(DB_URL)

    print('Creating tables.')
    db.create_all()
    print('Shiny! Ready to go')

@manager.command
def list_routes():
    """GET all routes registered in the app"""
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, rule))
        output.append(line)

    for line in sorted(output):
        print line

@manager.command
def import_all_days():
    inital_day = '2020-03-15'
    day = datetime.strptime(inital_day, '%Y-%m-%d').date()
    today = datetime.today().date()

    while True:
        datos(day.strftime("%Y-%m-%d"))
        if day == today:
            break
        day = day + timedelta(days=1)
        

if __name__ == "__main__":
    manager.run()