import os

from flask import Flask
from flask import render_template

def create_app(test_config=None):
    # create and configure the app
    app = Flask(
        __name__,
        instance_relative_config=True,
        static_url_path='', 
        static_folder='static',
        template_folder='templates',
    )
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass



    @app.route('/')
    def index():
        return render_template('index.html', title='Home')

    @app.route('/explore')
    def explore():
        return render_template('explore.html', title='Home')

    @app.route('/about')
    def about():
        return render_template('about.html', title='Home')

    @app.errorhandler(404)
    def page_not_found(error):
       return render_template('404.html', title = '404'), 400

    @app.errorhandler(500)
    def other_error(error):
       return render_template('404.html', title = '404'), 500

    return app
