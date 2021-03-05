from datetime import datetime
from flask import Flask, render_template,request, redirect
from sensor_data import current_ph, current_ec
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hydro.db'
db = SQLAlchemy(app)

plants = db.Table('plants',
    db.Column('plant_id', db.Integer, db.ForeignKey('plant.id'), primary_key=True),
    db.Column('enviro_id', db.Integer, db.ForeignKey('enviro.id'), primary_key=True),
    db.Column('plant_date', db.DateTime, default=datetime.utcnow)
)

class Pin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    num = db.Column(db.Integer)
    output = db.Column(db.Integer, default=0)
    gpio_pin = db.Column(db.Integer, nullable=False)

class Air(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    min_temp = db.Column(db.Integer, default=60)
    max_temp = db.Column(db.Integer, default=80)
    min_humid = db.Column(db.Integer, default=50)
    max_humid = db.Column(db.Integer, default=60)

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
    start_time = db.Column(db.String(10))
    end_time = db.Column(db.String(10))
    enviros = db.relationship('Enviro', backref='light', lazy=True)

    def __repr__(self):
        return '<Water %r>' % self.id

class Plant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Enviro(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    ph_sensor = db.Column(db.Integer, default=0)
    ec_sensor = db.Column(db.Integer, default=0)
    nutrient_solenoid = db.Column(db.Integer, default=0)
    ph_solenoid = db.Column(db.Integer, default=0)
    water_pump = db.Column(db.Integer, default=0)
    air_pump = db.Column(db.Integer, default=0)
    light_outlet = db.Column(db.Integer, default=0)
    active = db.Column(db.Integer, default=0)
    water_id = db.Column(db.Integer, db.ForeignKey('water.id'), nullable=False)
    light_id = db.Column(db.Integer, db.ForeignKey('light.id'), nullable=False)
    plants = db.relationship('Plant', secondary=plants, lazy='subquery',
        backref=db.backref('enviros', lazy=True))

    def current_ph(self):
        """Retrieves the current pH level of the water from the ph sensor attached to
        the current Enviro()
        """
        if self.ph_sensor == 0:
            return 'N/A'
        ph_level = current_ph(self.ph_sensor)
        return float(ph_level)

    def current_ec(self):
        """Retrieves the current EC level of the water from the ec sensor attached to
        the current Enviro()
        """
        if self.ec_sensor == 0:
            return 'N/A'
        ec_level = current_ec(self.ec_sensor)
        return float(ec_level)
    
    def alert_status(self, sensor):
        if sensor == "ph":
            if self.ph_sensor == 0:
                return
            if current_ph(self.ph_sensor) < self.water.min_ph or current_ph(self.ph_sensor) > self.water.max_ph:
                return "alert"
        if sensor == "ec":
            if self.ec_sensor == 0:
                return
            if current_ec(self.ec_sensor) < self.water.min_ec or current_ec(self.ec_sensor) > self.water.max_ec:
                return "alert"
