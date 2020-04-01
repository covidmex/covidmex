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
        self.created_at = datetime.now()
        self.status = data['status']
        self.age = data['age']
        self.sex = data['sex']
        self.type_contagion = data['type_contagion']
        self.state_id = data['state_id']
        self.country_procedence_id = data['country_procedence_id']

    def __repr__(self):
        return '<Case %s >' % self.created_at.strftime("%d/%m/%Y")

    @classmethod
    def update_time(self):
        max_date = db.session.query(func.max(self.created_at)).first()[0]
        return max_date

