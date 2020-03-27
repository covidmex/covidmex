from datetime import datetime

from sqlalchemy_utils import UUIDType

from .extensions import db

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    short_name = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<State %r>' % self.name

class CountryProcedence(db.Model):
    __tablename__ = 'country_procedence'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    short_name = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<Country %r>' % self.name

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key = True)
    synthomp_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    arrival_date_to_mexico= db.Column(db.DateTime, nullable=False, default=datetime.now())
    appearance_date= db.Column(db.DateTime, nullable=False, default=datetime.now())
    status = db.Column(db.String(255), unique=False, nullable=False)
    locality = db.Column(db.String(255), unique=False, nullable=True)
    contagion_type = db.Column(db.String(255), unique=False, nullable=False)
    sex = db.Column(db.String(255), unique=False, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    state = db.relationship("State")
    country_procedence_id = db.Column(db.Integer, db.ForeignKey('country_procedence.id'))
    country_procedence = db.relationship("CountryProcedence")

    def __repr__(self):
        return '<Case %r - >' % self.appearance_date, self.status