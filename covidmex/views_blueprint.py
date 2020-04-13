# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import json

from flask import Flask, jsonify, request
from flask import render_template
from flask import Blueprint
from datetime import datetime, timedelta
from sqlalchemy import or_


from models import State, Case, CountryProcedence, Totals, Fallecidos
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
    total_female_percentage = round((last_record.female * 100) / total_confirmed,1)
    total_male_percentage = round((last_record.male * 100) / total_confirmed,1)
    total_male = int(last_record.male)
    total_female = int(last_record.female)
    delta_confirmed = last_record.confirmed
    total_suspected = last_record.suspected
    total_death = last_record.death
    death_ratio = float((total_death*100) / total_confirmed)
    try:
        last_day_confirmed = previous_record.confirmed
        delta_confirmed = total_confirmed - last_day_confirmed
    except:
        delta_confirmed = 0
    increase_ratio = float((delta_confirmed*100) / previous_record.confirmed)
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
    confirmed_cases_by_state =  db.session.query(State.name, db.func.count(Case.status=='confirmed')).filter(Case.created_at == update_time, Case.status == 'confirmado').outerjoin(State).group_by(State.name).all()
    confirmed_cases_by_state.sort(key=lambda tup: tup[1], reverse=True)
    suspected_cases_by_state =  db.session.query(State.name, db.func.count(Case.status=='suspected')).filter(Case.created_at == update_time, Case.status == 'Sospechoso').outerjoin(State).group_by(State.name).all()
    suspected_cases_by_state.sort(key=lambda tup: tup[1], reverse=True)
    # Deaths by state
    total_deaths_by_state = db.session.query(Fallecidos).filter(Fallecidos.created_at == update_time).all()
    deaths_by_state = [[death.state, death.total] for death in total_deaths_by_state]

    _vars = {
        "confirmed_cases_by_state": confirmed_cases_by_state[0:10],
        "age_bars_labels": age_bars_labels,
        "age_bars_confirmed" : age_bars_confirmed,
        "histogram_labels": histogram_labels,
        "histogram_confirmed": histogram_confirmed,
        "histogram_suspects": histogram_suspects,
        "total_female_percentage": total_female_percentage,
        "total_male_percentage": total_male_percentage,
        "total_female": total_female,
        "total_male": total_male,
        "total_confirmed": total_confirmed,
        "total_suspected": total_suspected,
        "delta_confirmed": delta_confirmed,
        "death_ratio": death_ratio,
        "increase_ratio": increase_ratio,
        "total_death": total_death,
        "deaths_by_state": deaths_by_state,
        "update_time" : update_time.strftime("%d/%m/%Y")
    }
    return render_template(
        'index.html',
        vars=_vars,
    )


@views_blueprint.route('/explore')
def explore():
    update_time = Totals.update_time()
    _vars = {
        "update_time" : update_time.strftime("%d/%m/%Y")
    }
    return render_template(
        'explore.html',
        vars=_vars,
    )

@views_blueprint.route('/explore/cases', methods=['POST'])
def cases():

    params = request.form
    form = dict((k,v) for k,v in params.items() if v)

    aaData = []
    start = int(str(form.get("iDisplayStart")))
    display_length = int(str(form.get("iDisplayLength")))
    end = start + display_length
    search_0 = form.get('sSearch_0')
    search_1 = form.get('sSearch_1')
    search_2 = form.get('sSearch_2')
    search_3 = form.get('sSearch_3')
    search_4 = form.get('sSearch_4')
    search_5 = form.get('sSearch_5')
    search_6 = form.get('sSearch_6')
    search_7 = form.get('sSearch_7')

    update_time = Case.update_time()
    
    ORDER_BY_FIELDS = {
        0: 'username',
        1: 'email',
        2: 'is_active',
        4: 'date_joined',
    }
    all_cases = db.session.query(Case).join(State).join(CountryProcedence).filter(Case.created_at == update_time)
    if search_0:
        all_cases = all_cases.filter(State.name.like("%%%s%%" % search_0))

    if search_1:
        all_cases = all_cases.filter(Case.sex.like("%%%s%%" % search_1))

    if search_2:
        all_cases = all_cases.filter(Case.age.like("%%%s%%" % search_2))

    if search_3:
        all_cases = all_cases.filter(Case.symptom_date.like("%%%s%%" % search_3))

    if search_4:
        all_cases = all_cases.filter(Case.status.like("%%%s%%" % search_4))

    if search_5:
        all_cases = all_cases.filter(Case.type_contagion.like("%%%s%%" % search_5))

    if search_6:
        all_cases = all_cases.filter(CountryProcedence.name.like("%%%s%%" % search_6))

    if search_7:
        all_cases = all_cases.filter(Case.arrival_to_mexico.like("%%%s%%" % search_7))



    all_cases.all()
    count = all_cases.count()
    """
    if sort:
        direction = '-' if request.POST.get('sSortDir_0') == 'desc' else '' # asc or desc?
        index_of_field = int(sort) # order by which field?
        order_statment = direction + ORDER_BY_FIELDS.get(index_of_field)
        users = users.order_by(order_statment)
    """

    aaData = [(case.to_dict()) for case in all_cases[start:end]]
    data = {
        "iTotalRecords": count,
        "iDisplayStart": start,
        "iDisplayLength": display_length,
        "iTotalDisplayRecords": count,
        "aaData":aaData
    }
    return  json.dumps(data)


@views_blueprint.route('/about')
def about():
    update_time = Totals.update_time()
    _vars = {
        "update_time" : update_time.strftime("%d/%m/%Y")
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
            label = '0-9'
        if i == 10:
            label = '10-19'
        if i == 20:
            label = '20-29'
        if i == 30:
            label = '30-39'
        if i == 40:
            label = '40-49'
        if i == 50:
            label = '50-59'
        if i == 60:
            label = '60-69'
        if i == 70:
            label = '70-79'
        if i == 80:
            label = '80-89'
        if i == 90:
            label = '90-99'
        age_bars_labels.append(label)
    return age_bars_labels


