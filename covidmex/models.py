from sqlalchemy import func, and_
from datetime import datetime

from .extensions import db

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    short_name = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, name = None, short_name=None):
        self.name = name
        self.short_name = name

    def __repr__(self):
        return '<State %r>' % self.name

class CountryProcedence(db.Model):
    __tablename__ = 'country_procedence'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    short_name = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, name = None, short_name=None):
        self.name = name
        self.short_name = name

    def __repr__(self):
        return '<CountryProcedence %r>' % self.name

class Totals(db.Model):
    __tablename__ = 'totals'
    id = db.Column(db.Integer, primary_key = True)
    suspected = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    confirmed = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    recovery = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    death = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    death_rate = db.Column(db.Float, nullable=True, server_default=db.text("0"))
    recovery_rate = db.Column(db.Float, nullable=True, server_default=db.text("0"))
    male = db.Column(db.Float, nullable=True, server_default=db.text("0"))
    female = db.Column(db.Float, nullable=True, server_default=db.text("0"))
    new_cases = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    new_deaths = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    imported = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    locally = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
 
    def __repr__(self):
        return '<Totals %r>' % self.id

    def __init__(self, data):
        self.suspected = data['suspected']
        self.confirmed = data['confirmed']
        self.created_at = data['created_at']
        if 'recovery' in data:
            self.recovery = data['recovery']
            if data['confirmed'] > 0 and data['recovery'] > 0:
                self.recovery_rate = int(data['recovery']) / int(data['confirmed']) 
        if 'death' in data:
            self.death = data['death']
            if data['confirmed'] > 0 and data['death_rate'] > 0:
                self.death_rate = int(data['death_rate']) / int(data['confirmed']) 
        if 'new_cases' in data:
            self.new_cases = data['new_cases']
        if 'new_deaths' in data:
            self.new_deaths = data['new_deaths']
        self.imported = data['imported']
        self.locally = data['locally']
        self.male = data['male']
        self.female = data['female']

    def to_dict(self):
        data = list()
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                value = getattr(self, key)
                # If the value is a datetime object, get the string
                if  isinstance(value, datetime):
                    value = value.strftime("%d/%m/%Y")
                data.append((key, value))
        return dict(data)

    @classmethod
    def update_time(self):
        max_date = db.session.query(func.max(self.created_at)).first()[0]
        return max_date.date()


class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key = True)
    case_number = db.Column(db.String(10), nullable=False)
    symptom_date = db.Column(db.DateTime, nullable=False,  server_default=db.text("CURRENT_TIMESTAMP"))
    arrival_to_mexico= db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    created_at= db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    status = db.Column(db.String(50), unique=False, nullable=False)
    locality = db.Column(db.String(255), unique=False, nullable=True)
    age = db.Column(db.String(5), unique=False, nullable=True)
    sex = db.Column(db.Enum('M', 'F', 'O', name='sex'), server_default=db.text("'O'"))
    type_contagion = db.Column(db.Enum('contacto', 'importado', name='type_contagion'), nullable=True)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    country_procedence_id = db.Column(db.Integer, db.ForeignKey('country_procedence.id'))

    state = db.relationship("State")
    country_procedence = db.relationship("CountryProcedence")

    def __init__(self,data):
        self.case_number = data['case_number']
        self.symptom_date = data['symptom_date']
        self.arrival_to_mexico = data['arrival_to_mexico']
        self.created_at = data['created_at']
        self.status = data['status']
        self.age = data['age']
        self.sex = data['sex']
        self.type_contagion = data['type_contagion']
        self.state_id = data['state_id']
        self.country_procedence_id = data['country_procedence_id']

    def __repr__(self):
        return '<Case %s >' % self.created_at.strftime("%d/%m/%Y")

    def to_dict(self):
        data = list()
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                value = getattr(self, key)
                # If the value is a datetime object, get the string
                if  isinstance(value, datetime):
                    value = value.strftime("%d/%m/%Y")
                # If the value is a relationship from state, get the string
                if  key == 'state_id':
                    value = self.state.name
                    key = 'state'
                # If the value is a relationship from Country, get the string
                if  key == 'country_procedence_id':
                    value = self.country_procedence.name
                    key = 'country_procedence'

                data.append((key, value))
        return dict(data)

    @classmethod
    def update_time(self):
        max_date = db.session.query(func.max(self.created_at)).first()[0]
        return max_date.date()


class Fallecidos(db.Model):
    __tablename__ = 'fatalities'
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(200), nullable=False)
    total = db.Column(db.Integer, nullable=True, server_default=db.text("0"))
    created_at = db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))

    def __init__(self, data, fecha):
        self.state = data['Estado']
        self.total = data['Fallecidos']
        self.created_at = fecha

    def __repr__(self):
        return '<Fallecidos %s >' % self.id

    def to_dict(self):
        data = list()
        for key in self.__dict__.keys():
            if not key.startswith("_"):
                value = getattr(self, key)
                data.append((key, value))
        return dict(data)


class Entidad(db.Model):
    __tablename__ = 'entidades'

    CLAVE_ENTIDAD = db.Column(db.Integer, primary_key=True)
    ENTIDAD_FEDERATIVA = db.Column(db.String(31), nullable=False)
    ABREVIATURA = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<Entidad %r>' % self.CLAVE_ENTIDAD

class Municipio(db.Model):
    __tablename__ = 'municipios'

    ID = db.Column(db.Integer, primary_key=True)
    CLAVE_ENTIDAD = db.Column(db.String(5), nullable=False)
    ENTIDAD_FEDERATIVA = db.Column(db.String(100), nullable=False)
    ABREVIATURA = db.Column(db.String(3), nullable=False)

    def __repr__(self):
        return '<Municipio %r>' % self.Id

class OficialCase(db.Model):
    __tablename__ = 'oficial_cases'

    ID = db.Column(db.Integer, primary_key=True)
    FECHA_ACTUALIZACION = db.Column(db.Date)
    ORIGEN = db.Column(db.Integer, nullable=True)
    SECTOR = db.Column(db.Integer, nullable=True)
    ENTIDAD_UM = db.Column(db.Integer, nullable=True)
    SEXO = db.Column(db.Integer, nullable=True)
    ENTIDAD_NAC = db.Column(db.Integer, nullable=True)
    ENTIDAD_RES = db.Column(db.Integer, nullable=True)
    MUNICIPIO_RES = db.Column(db.Integer, nullable=True)
    TIPO_PACIENTE = db.Column(db.Integer, nullable=True)
    FECHA_INGRESO = db.Column(db.Date, nullable=True)
    FECHA_SINTOMAS = db.Column(db.Date, nullable=True)
    FECHA_DEF = db.Column(db.Date, nullable=True)
    INTUBADO = db.Column(db.Integer, nullable=True)
    NEUMONIA = db.Column(db.Integer, nullable=True)
    EDAD = db.Column(db.Integer, nullable=True)
    NACIONALIDAD = db.Column(db.Integer, nullable=True)
    EMBARAZO = db.Column(db.Integer, nullable=True)
    HABLA_LENGUA_INDIG = db.Column(db.Integer, nullable=True)
    DIABETES = db.Column(db.Integer, nullable=True)
    EPOC = db.Column(db.Integer, nullable=True)
    ASMA = db.Column(db.Integer, nullable=True)
    INMUSUPR = db.Column(db.Integer, nullable=True)
    HIPERTENSION = db.Column(db.Integer, nullable=True)
    OTRA_COM = db.Column(db.Integer, nullable=True)
    CARDIOVASCULAR = db.Column(db.Integer, nullable=True)
    OBESIDAD = db.Column(db.Integer, nullable=True)
    RENAL_CRONICA = db.Column(db.Integer, nullable=True)
    TABAQUISMO = db.Column(db.Integer, nullable=True)
    OTRO_CASO = db.Column(db.Integer, nullable=True)
    RESULTADO = db.Column(db.Integer, nullable=True)
    MIGRANTE = db.Column(db.Integer, nullable=True)
    PAIS_NACIONALIDAD = db.Column(db.String(250), nullable=True)
    PAIS_ORIGEN = db.Column(db.String(250), nullable=True)
    UCI = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        return '<OficialCase %r>' % self.ID

    def __init__(self, d):
        self.FECHA_ACTUALIZACION = d[0]
        self.ORIGEN = d[1]
        self.SECTOR = d[2]
        self.ENTIDAD_UM =d[3]
        self.SEXO =d[4]
        self.ENTIDAD_NAC = d[5]
        self.ENTIDAD_RES = d[6]
        if isinstance(d[7], int):
            self.MUNICIPIO_RES = d[7]
        self.TIPO_PACIENTE = d[8]

        if d[9] != '9999-99-99':
            self.FECHA_INGRESO =d[9]

        if d[10] != '9999-99-99':
            self.FECHA_SINTOMAS = d[10]
        
        if d[11] != '9999-99-99': 
            self.FECHA_DEF = d[11]
        self.INTUBADO = d[12]
        self.NEUMONIA = d[13]
        self.EDAD = d[14]
        self.NACIONALIDAD =d[15]
        self.EMBARAZO = d[16]
        self.HABLA_LENGUA_INDIG = d[17]
        self.DIABETES = d[18]
        self.EPOC = d[19]
        self.ASMA = d[20]
        self.INMUSUPR = d[21]
        self.HIPERTENSION = d[22]
        self.OTRA_COM = d[23]
        self.CARDIOVASCULAR = d[24]
        self.OBESIDAD = d[25]
        self.RENAL_CRONICA = d[26]
        self.TABAQUISMO = d[27]
        self.OTRO_CASO = d[28]
        self.RESULTADO = d[29]
        self.MIGRANTE = d[30]
        self.PAIS_NACIONALIDAD = d[31]
        self.PAIS_ORIGEN = d[32]
        self.UCI = d[33]

class Origen(db.Model):
    __tablename__ = 'origen'

    CLAVE = db.Column(db.Integer, primary_key=True)
    DESCRIPCION = db.Column(db.String(15), nullable=False)

    def __repr__(self):
        return '<Origen %r>' % self.CLAVE

class Resultado(db.Model):
    __tablename__ = 'resultado'

    CLAVE = db.Column(db.Integer, primary_key=True)
    DESCRIPCION = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return '<Resultado %r>' % self.CLAVE

class Sector(db.Model):
    __tablename__ = 'sector'

    CLAVE = db.Column(db.Integer, primary_key=True)
    DESCRIPCION = db.Column(db.String(100), nullable=False)


class Sexo(db.Model):
    __tablename__ = 'sexo'

    CLAVE = db.Column(db.Integer, primary_key=True)
    DESCRIPCION = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<Sexo %r>' % self.CLAVE

class SiNo(db.Model):
    __tablename__ = 'si_no'

    CLAVE = db.Column(db.Integer, primary_key=True)
    DESCRIPCION = db.Column(db.String(25), nullable=False)


class TipoPaciente(db.Model):
    __tablename__ = 'tipo_paciente'

    CLAVE = db.Column(db.Integer, primary_key=True)
    DESCRIPCION = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return '<TipoPaciente %r>' % self.CLAVE


