from datetime import datetime
from flask import Flask, render_template,request, redirect
from sensor_data import current_ph, current_ec
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydro.db'
db = SQLAlchemy(app)

class Water(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    min_ph = db.Column(db.Float, default=5.5)
    max_ph = db.Column(db.Float, default=6.5)
    min_ec = db.Column(db.Float, default=1.2)
    max_ec = db.Column(db.Float, default=1.6)
    enviros = db.relationship('Enviro', backref='water', lazy=True)

    def __repr__(self):
        return '<Water %r>' % self.id

class Light(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    model = db.Column(db.String(50))
    start_time = db.Column(db.Time)
    end_time = db.Column(db.Time)
    enviros = db.relationship('Enviro', backref='light', lazy=True)

    def __repr__(self):
        return '<Water %r>' % self.id

class Enviro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ph_sensor = db.Column(db.Integer, default=0)
    ec_sensor = db.Column(db.Integer, default=0)
    ec_solenoid = db.Column(db.Integer, default=0)
    ph_solenoid = db.Column(db.Integer, default=0)
    water_pump = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, default=0)
    water_id = db.Column(db.Integer, db.ForeignKey('water.id'), nullable=False)
    light_id = db.Column(db.Integer, db.ForeignKey('light.id'), nullable=False)

    def current_ph(self):
        """Retrieves the current pH level of the water from the ph sensor attached to
        the current Enviro()
        """
        ph_level = current_ph(self.ph_sensor)
        return ph_level