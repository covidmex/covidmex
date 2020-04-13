from flask import Flask, Blueprint, jsonify, request
from models import State, Case, CountryProcedence, Totals, Fallecidos
from sqlalchemy import func, and_
from extensions import db
import json
from datetime import date, datetime

totals_api = Blueprint('totals_api', __name__)

@totals_api.route("/", methods = ['GET'])
def init(day=None):
  return jsonify({
      "data": 'No data',
      "code": "204",
      "success" : "false"
    }),200


@totals_api.route("/daily", methods = ['GET'])
@totals_api.route("/daily/<string:day>", methods = ['GET'])
def dailyGlobal(day=None):
  if day is None:
    day = str(date.today())
  
  data = getDailyTotal(day)
  
  if data:
    return jsonify({
      "data": data,
      "code": "200",
      "success" : "true"
    }),200
  else:
    return jsonify({
      "data": 'No data',
      "code": "204",
      "success" : "false"
    }),200


def getDailyTotal(day, day2 = None):
  data = {}
  if day2 is None:
    resp = db.session.query(Totals).filter(func.DATE(Totals.created_at) == day).first()
    fall = db.session.query(func.sum(Fallecidos.total)).filter(func.DATE(Fallecidos.created_at) == day).first()
    if resp:
      data['suspected'] = int(resp.suspected)
      data['confirmed'] = int(resp.confirmed)
      data['day'] = str(resp.created_at)
      data['male'] = int(resp.male)
      data['female'] = int(resp.female)
      data['deaths'] = int(fall[0])
      data['new_deaths'] = int(resp.new_deaths)
      data['new_cases'] = int(resp.new_cases)
      data['lethality'] = round(float(fall[0]) / float(resp.confirmed) * 100,2)
  
  if day2 is not None:
    print("day 2")
    resp = db.session.query(Totals).filter(and_(func.DATE(Totals.created_at) >= day),func.DATE(Totals.created_at) <= day2)
    print(resp)
    print(resp.count())
    if resp.count() > 0:
      data2 = {}
      for r in resp:
        fall = db.session.query(func.sum(Fallecidos.total)).filter(func.DATE(Fallecidos.created_at) == func.DATE(r.created_at)).first()
        
        data2['suspected'] = int(r.suspected)
        data2['confirmed'] = int(r.confirmed)
        data2['day'] = str(r.created_at)
        data2['male'] = int(r.male)
        data2['female'] = int(r.female)
        data2['new_deaths'] = int(r.new_deaths)
        data2['new_cases'] = int(r.new_cases)
        if fall:
          data2['deaths'] = int(fall[0])
          data2['lethality'] = round(float(fall[0]) / float(r.confirmed) * 100,2)
        else:
          data2['deaths'] = 0
          data2['lethality'] = 0

        key = str(r.created_at).split(" ")[0]
        data[key] = data2

  return data


@totals_api.route("/daily/<string:day>/<string:tipo>", methods = ['GET'])
def dailyByType(day=None, tipo=None):
    if day is None:
      day = str(date.today())
    if tipo is None:
      return jsonify({
        "data": 'No data',
        "code": "204",
        "success" : "false"
      }),200
    data = {}
    if tipo == 'confirmed' or tipo == 'deaths' or tipo == 'suspected':
      if tipo == 'confirmed':
        letter = 'c'
      if tipo == 'suspected':
        letter = 's'
      if tipo == 'deaths':
        letter = 'f'
      
      f = 'json/'+day+'-'+letter+'.json'

      with open(f) as datos:
        data = json.load(datos)
    else:
      return jsonify({
        "data": 'No tipo recognized (confirmed, deaths or suspected)',
        "code": "204",
        "success" : "false"
      }),200


    return jsonify({
      "data": data,
      "code": "200",
      "success" : "true"
    }),200



@totals_api.route("/between/<string:day>/<string:day2>", methods = ['GET'])
def dailyGlobalBetween(day=None, day2=None):
  if day is None:
    day = str(date.today())

  if day2 is None:
    day2 = str(date.today())
  
  data = getDailyTotal(day, day2)
  
  if data:
    return jsonify({
      "data": data,
      "code": "200",
      "success" : "true"
    }),200
  else:
    return jsonify({
      "data": 'No data',
      "code": "204",
      "success" : "false"
    }),200