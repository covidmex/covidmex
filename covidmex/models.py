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


class TypeContagion(db.Model):
    __tablename__ = 'type_contagion'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100), unique=False, nullable=False)
    description = db.Column(db.String(255), unique=False, nullable=True)

    def __init__(self, name = None, description=None):
        self.name = name
        self.description = name

    def __repr__(self):
        return '<TypeContagion %r>' % self.name

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key = True)
    symptom_date = db.Column(db.DateTime, nullable=False,  server_default=db.text("CURRENT_TIMESTAMP"))
    arrival_to_mexico= db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    created_at= db.Column(db.DateTime, nullable=False, server_default=db.text("CURRENT_TIMESTAMP"))
    status = db.Column(db.String(50), unique=False, nullable=False)
    locality = db.Column(db.String(255), unique=False, nullable=True)
    sex = db.Column(db.Enum('M', 'F', 'O', name='sex'), server_default=db.text("'O'"))
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    country_procedence_id = db.Column(db.Integer, db.ForeignKey('country_procedence.id'))
    type_contagion_id = db.Column(db.Integer, db.ForeignKey('type_contagion.id'))

    state = db.relationship("State")
    country_procedence = db.relationship("CountryProcedence")
    type_contagion = db.relationship("TypeContagion")

    def __init__(self, symptom_date=None, arrival_to_mexico=None, status=None,
            locality=None, sex=None, state_id=None, country_procedence_id=None, type_contagion_id=None):
        self.symptom_date = symptom_date
        self.arrival_to_mexico = arrival_to_mexico
        self.created_at = datetime.datetime.now()
        self.status = status
        self.locality = locality
        self.sex = sex
        self.state_id = state_id
        self.country_procedence_id = country_procedence_id
        self.type_contagion_id = type_contagion_id

    def __repr__(self):
        return '<Case %r - >' % self.appearance_date, self.status