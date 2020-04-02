from flask import Flask, Blueprint, jsonify, request
from datetime import date
import json, datetime
from covidmex.models import State, Case, CountryProcedence, Totals
from .extensions import db

import_api = Blueprint('import_api', __name__)

@import_api.route("/import", methods = ['GET'])
def datos(day=None):

  day = '2020-03-22'
  #What day is today?
  if day is None:
    day = date.today().strftime("%Y-%m-%d") 

  #files name
  path = 'json/'
  files = [path+day+'-s.json', path+day+'-c.json']
  
  #Read all data
  a = []
  for f in files:
    with open(f) as datos:
      data = json.load(datos)
      for d in data['datos']:
        a.append(d)

  #import data to tables
  resp = adding(a, day)
  db.session.commit()

  return jsonify({
            "success": True,
            "code": 200,
            "data": "imported "+day+" /  "+resp
            }
        ), 200

def adding(data, day):
  #Interation to insert
  totals = 0
  imported = 0
  suspected = 0
  male = 0
  female = 0
  for d in data:
    #identify state
    state_id = identifyState(d)
    contagion_type = identifyTypeContagion(d)
    country_id = identifyCountryProcedence(d)
    addCase(d, state_id, contagion_type, country_id, day)
    totals += 1
    if contagion_type == 'importado':
      imported += 1
    
    if d['rt-pcr'].upper() == 'SOSPECHOSO':
      suspected += 1
    
    if d['sexo'].upper() == 'M' and d['rt-pcr'].upper() == 'CONFIRMADO':
      male += 1
    elif d['sexo'].upper() == 'F' and d['rt-pcr'].upper() == 'CONFIRMADO':
      female += 1

  data = {
    'totals': totals,
    'suspected': suspected,
    'confirmed': totals - suspected, 
    'imported': imported,
    'locally': totals - imported,
    'male': male,
    'female': female,
    'created_at': day
  }
  addTotals(data)

  return str(totals)


def addTotals(data):
  newTotals = Totals(data)
  db.session.add(newTotals)


def identifyState(d):
  state = db.session.query(State).filter(State.name == d['estado'])
  if state.count() == 1:
    state_id = state[0].id
  else:
    newState = State(d['estado'],d['estado'])
    db.session.add(newState)
    db.session.commit()
    state_id = newState.id
  return state_id


def identifyTypeContagion(d):
  if d['procedencia'].lower() == 'contacto':
    return 'contacto'
  else:
    return 'importado'


def identifyCountryProcedence(d):
  country = db.session.query(CountryProcedence).filter(CountryProcedence.name == d['procedencia'])
  if country.count() == 1:
    country_id = country[0].id
  else:
    newCountry = CountryProcedence(d['procedencia'],d['procedencia'])
    db.session.add(newCountry)
    db.session.commit()
    country_id = newCountry.id
  return country_id 


def addCase(d, state, contagionType, country, day):
  
  try:
    symptom = datetime.datetime.strptime(d['sintomas'], '%d/%m/%Y')
  except:
    symptom = None

  if d['llegada'] == 'NA':
    llegada = None
  else:
    try:
      llegada = datetime.datetime.strptime(d['llegada'],'%d/%m/%Y')
    except:
      llegada = None
  
  if d['sexo'].upper() == 'M' or d['sexo'].upper() == 'F':
    sexo = d['sexo'].upper()
  else:
    sexo = 'O'
  newCase = Case({
    'created_at': day,
    'case_number' : d['caso'],
    'symptom_date' : symptom, 
    'arrival_to_mexico' : llegada, 
    'status' : d['rt-pcr'],
    'age' : d['edad'],
    'sex' : sexo, 
    'state_id' : state, 
    'country_procedence_id' : country, 
    'type_contagion' : contagionType
  })
    
  db.session.add(newCase)
