from datetime import datetime

from sqlalchemy_utils import UUIDType

from .extensions import db

class Sex(db.Model):
    __tablename__ = 'sex'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    short_ame = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<Sex %r>' % self.name

class State(db.Model):
    __tablename__ = 'states'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    short_name = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<State %r>' % self.name

class TypeContagion(db.Model):
    __tablename__ = 'type_contagions'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    description = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<TypeContagion %r>' % self.name

class LoadData(db.Model):
    __tablename__ = 'load_data'
    id = db.Column(db.Integer, primary_key = True)
    date= db.Column(db.DateTime, nullable=False, default=datetime.now())
    origin = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<LoadData %r>' % self.name

class Country(db.Model):
    __tablename__ = 'countries'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255), unique=False, nullable=True)
    short_name = db.Column(db.String(255), unique=False, nullable=True)

    def __repr__(self):
        return '<Country %r>' % self.name

class Case(db.Model):
    __tablename__ = 'cases'
    id = db.Column(db.Integer, primary_key = True)
    synthomp_date = db.Column(db.DateTime, nullable=False, default=datetime.now())
    confirmed = db.Column(db.Boolean, unique=False, default=False)
    date= db.Column(db.DateTime, nullable=False, default=datetime.now())
    pcr = db.Column(db.Integer, default = 0)
    locality = db.Column(db.String(255), unique=False, nullable=True)
    type_contagion_id = db.Column(db.Integer, db.ForeignKey('type_contagions.id'))
    type_contagion = db.relationship("TypeContagion")
    state_id = db.Column(db.Integer, db.ForeignKey('states.id'))
    state = db.relationship("State")
    sex_id = db.Column(db.Integer, db.ForeignKey('sex.id'))
    sex = db.relationship("Sex")
    load_data_id = db.Column(db.Integer, db.ForeignKey('load_data.id'))
    load_data = db.relationship("LoadData")
    country_id = db.Column(db.Integer, db.ForeignKey('countries.id'))
    country = db.relationship("Country")

    def __repr__(self):
        return '<Case %r>' % self.email