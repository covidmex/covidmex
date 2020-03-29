from flask import Flask, Blueprint, jsonify, request
from datetime import date
import json, datetime
from covidmex.models import State, Case, CountryProcedence
from .extensions import db

import_api = Blueprint('import_api', __name__)

@import_api.route("/import", methods = ['GET'])
def datos(day=None):

  day = '2020-03-26'
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
  resp = adding(a)

  return jsonify({
            "success": True,
            "code": 200,
            "data": "imported "+day+" /  "+resp
            }
        ), 200

def adding(data):
  #Interation to insert
  for d in data:
    #identify state
    state_id = identifyState(d)
    contagion_type = identifyTypeContagion(d)
    country_id = identifyCountryProcedence(d)
    addCase(d, state_id, contagion_type, country_id)
  return 'registros importados'

def identifyState(d):
  state = db.session.query(State).filter(State.name == d['estado'])
  if state.count() == 1:
    state_id = state[0].id
  else:
    newState = State(d['estado'],d['estado'])
    db.session.add(newState)
    db.session.flush()
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
    db.session.flush()
    db.session.commit()
    country_id = newCountry.id
  return country_id 

def addCase(d, state, contagionType, country):
  
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
    'case_number' : d['Caso'],
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
  db.session.flush()
  db.session.commit()