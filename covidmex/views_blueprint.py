# -*- coding: utf-8 -*-
import os
import json

from flask import Flask, jsonify
from flask import render_template
from flask import Blueprint
from datetime import datetime, timedelta


from models import State, Case, CountryProcedence, Totals
from extensions import db

views_blueprint = Blueprint('views_blueprint', __name__)



@views_blueprint.route('/')
def index():
    all_totals = db.session.query(Totals).order_by(Totals.created_at.asc()).all()
    # Histogram
    histogram_labels = [(total.to_dict()['created_at']) for total in all_totals]
    histogram_confirmed = [(total.to_dict()['confirmed']) for total in all_totals]
    histogram_suspects = [(total.to_dict()['suspected']) for total in all_totals]
    # All totals
    update_time = Totals.update_time()
    yesterday =  update_time + timedelta(days=-1)
    last_record = db.session.query(Totals).filter(Totals.created_at == update_time).first()
    previous_record = db.session.query(Totals).filter(Totals.created_at == yesterday).first()
    total_confirmed = last_record.confirmed
    total_suspected = last_record.suspected
    last_day_confirmed = previous_record.confirmed
    delta_confirmed = total_confirmed - last_day_confirmed
    # Cases clasified by age
    all_ages_tuples = db.session.query(Case.age).filter(Case.created_at == update_time, Case.status == 'confirmado').all()
    all_ages = [value for value, in all_ages_tuples]
    clasified_ages = clasify_ages(all_ages)
    age_bars_numeric = list()
    age_bars_confirmed = list()
    for k,v in sorted(clasified_ages.items()):
        age_bars_numeric.append(k)
        age_bars_confirmed.append(v)
    age_bars_labels = get_labels(age_bars_numeric)
    # Confirmed cases by state
    cases_by_state =  db.session.query(State.name, db.func.count(Case.status=='confirmed')).filter(Case.created_at == update_time, Case.status == 'confirmado').outerjoin(State).group_by(State.name).all()
    cases_by_state.sort(key=lambda tup: tup[1], reverse=True)
    """donut_confirmed = list()
    donut_labels = list()
    for state, num_cases in cases_by_state[0:5]:
        donut_labels.append(state)
        donut_confirmed.append(num_cases)
    """
    _vars = {
        "cases_by_state": cases_by_state[0:10],
        "age_bars_labels": age_bars_labels,
        "age_bars_confirmed" : age_bars_confirmed,
        "histogram_labels": histogram_labels,
        "histogram_confirmed": histogram_confirmed,
        "histogram_suspects": histogram_suspects,
        "total_confirmed": total_confirmed,
        "total_suspected": total_suspected,
        "delta_confirmed": delta_confirmed,
        "update_time" : update_time.strftime("%d de %B de %Y")
    }
    return render_template(
        'index.html',
        vars=_vars,
    )


@views_blueprint.route('/explore')
def explore():
    update_time = Totals.update_time()
    _vars = {
        "update_time" : update_time.strftime("%d de %B de %Y")
    }
    return render_template(
        'explore.html',
        vars=_vars,
    )

@views_blueprint.route('/explore/cases')
def cases():
    update_time = Case.update_time()
    all_cases = db.session.query(Case).filter(Case.created_at == update_time).all()
    data = {'data' : [(case.to_dict()) for case in all_cases]}

    return  data


@views_blueprint.route('/about')
def about():
    update_time = Totals.update_time()
    _vars = {
        "update_time" : update_time.strftime("%d de %B de %Y")
    }
    return render_template(
        'about.html',
        vars=_vars,
    )

@views_blueprint.errorhandler(404)
def page_not_found(error):
   return render_template('404.html', title = '404'), 400

@views_blueprint.errorhandler(500)
def other_error(error):
   return render_template('404.html', title = '404'), 500


############################
#### Helpers to views ######
############################

def clasify_ages(all_ages):
    clasified_ages = dict()
    for age in all_ages:
        if age >= '0' and age < '10':
            key = 0
        if age >= '10' and age < '20':
            key = 10
        if age >= '20' and age < '30':
            key = 20
        if age >= '30' and age < '40':
            key = 30
        if age >= '40' and age < '50':
            key = 40
        if age >= '50' and age < '60':
            key = 50
        if age >= '60' and age < '70':
            key = 60
        if age >= '70' and age < '80':
            key = 70
        if age >= '80' and age < '90':
            key = 80
        if age >= '90' and age < '100':
            key = 90

        if key in clasified_ages:
            clasified_ages[key] += 1
        else:
            clasified_ages[key] = 1

    return clasified_ages

def get_labels(age_bars_numeric):
    age_bars_labels = list()
    for i in age_bars_numeric:
        if i == 0:
            label = '0-10'
        if i == 10:
            label = '10-20'
        if i == 20:
            label = '20-30'
        if i == 30:
            label = '30-40'
        if i == 40:
            label = '40-50'
        if i == 50:
            label = '50-60'
        if i == 60:
            label = '60-70'
        if i == 70:
            label = '70-80'
        if i == 80:
            label = '80-90'
        if i == 90:
            label = '90-110'
        age_bars_labels.append(label)
    return age_bars_labels
