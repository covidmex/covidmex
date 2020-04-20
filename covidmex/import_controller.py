from flask import Flask, Blueprint, jsonify, request
from datetime import date
import json, datetime, csv
from covidmex.models import OficialCase
from .extensions import db

import_api = Blueprint('import_api', __name__)

@import_api.route("/import", methods = ['GET'])
def datos(day=None):

  day = '2020-04-18'
  #What day is today?

  if day is None:
    day = date.today().strftime("%Y-%m-%d") 

  #files name
  path = 'datos_abiertos_gob/dataset/'
  files = path+day+'.csv'
  a = []
  #Read all data
  with open(files) as csv_file:
    reader = csv.reader(csv_file)
    for row in reader:
      a.append(row)

  #import data to tables
  adding(a)
  db.session.commit()

  return jsonify({
            "success": True,
            "code": 200,
            "data": "imported "+day
            }
        ), 200


def adding(data):
  
  for d in data:
    newCase = OficialCase(d)
    db.session.add(newCase)

###
# "FECHA_ACTUALIZACION",
# "ORIGEN",
# "SECTOR",
# "ENTIDAD_UM",
# "SEXO",
# "ENTIDAD_NAC",
# "ENTIDAD_RES",
# "MUNICIPIO_RES",
# "TIPO_PACIENTE",
# "FECHA_INGRESO",
# "FECHA_SINTOMAS",
# "FECHA_DEF",
# "INTUBADO",
# "NEUMONIA",
# "EDAD",
# "NACIONALIDAD",
# "EMBARAZO",
# "HABLA_LENGUA_INDIG",
# "DIABETES",
# "EPOC",
# "ASMA",
# "INMUSUPR",
# "HIPERTENSION",
# "OTRA_COM",
# "CARDIOVASCULAR",
# "OBESIDAD",
# "RENAL_CRONICA",
# "TABAQUISMO",
# "OTRO_CASO",
# "RESULTADO",
# "MIGRANTE",
# "PAIS_NACIONALIDAD",
# "PAIS_ORIGEN",
# "UCI"