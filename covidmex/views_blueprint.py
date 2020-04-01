# -*- coding: utf-8 -*-
import os
import json

from flask import Flask, jsonify
from flask import render_template
from flask import Blueprint


from models import State, Case, CountryProcedence
from extensions import db

views_blueprint = Blueprint('views_blueprint', __name__)



@views_blueprint.route('/')
def index():
    return render_template('index.html', title='Home')

@views_blueprint.route('/explore')
def explore():
    update_time = Case.update_time()
    return render_template(
        'explore.html',
        title='Home',
        update_time = update_time
    )

@views_blueprint.route('/explore/cases')
def cases():
    update_time = Case.update_time()
    all_cases = db.session.query(Case).filter(Case.created_at == update_time).all()
    data = {'data' : [(case.to_dict()) for case in all_cases]}

    return  data


@views_blueprint.route('/about')
def about():
    return render_template('about.html', title='Home')

@views_blueprint.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 400

@views_blueprint.errorhandler(500)
def other_error(error):
   return render_template('404.html', title = '404'), 500