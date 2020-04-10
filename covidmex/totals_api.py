from flask import Flask, Blueprint, jsonify, request
from models import State, Case, CountryProcedence, Totals, Fallecidos
from sqlalchemy import func
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


def getDailyTotal(day):
  resp = db.session.query(Totals).filter(func.DATE(Totals.created_at) == day).first()
  fall = db.session.query(func.sum(Fallecidos.total)).filter(func.DATE(Fallecidos.created_at) == day).first()
  data = {}
  
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


