# -*- coding: utf-8 -*-

import os
from datetime import datetime

from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from sqlalchemy_utils import database_exists, create_database, drop_database


from covidmex import create_app
from covidmex.extensions import db
from covidmex.models import Sex, State, TypeContagion, LoadData, Country, ConfirmedCase
from covidmex.config import DefaultConfig


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


if __name__ == "__main__":
    manager.run()