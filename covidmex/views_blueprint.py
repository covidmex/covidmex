import os

from flask import Flask
from flask import render_template
from flask import Blueprint

views_blueprint = Blueprint('views_blueprint', __name__)

@views_blueprint.route('/')
def index():
    return render_template('index.html', title='Home')

@views_blueprint.route('/explore')
def explore():
    return render_template('explore.html', title='Home')

@views_blueprint.route('/about')
def about():
    return render_template('about.html', title='Home')

@views_blueprint.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 400

@views_blueprint.errorhandler(500)
def other_error(error):
   return render_template('404.html', title = '404'), 500