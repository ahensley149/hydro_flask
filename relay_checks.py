#!/usr/bin/env python3

from models import *
from datetime import datetime
import RPi.GPIO as GPIO
from water_pump_check import *

enviros = Enviro.query.filter(Enviro.active == 1)
now = datetime.now()
current_time = now.strftime('%H:%M')


GPIO.setmode(GPIO.BOARD)

def lights_on(lights):
  """Turns the lights on
  """
  GPIO.output(lights, 1)


def enviro_check():
    for enviro in enviros:
        if enviro.light_outlet > 0:
            GPIO.setup(enviro.light_outlet, GPIO.OUT)
            light_start = enviro.light.start_time
            light_end = enviro.light.end_time
            if current_time > light_start and current_time < light_end:
                if GPIO.input(enviro.light_outlet) < 1:
                    lights_on(enviro.light_outlet)
        for cycle in enviro.water.cycles:
            cycle_start = cycle.start_time
            cycle_end = cycle.start_time
            if current_time > cycle_start and current_time < cycle_end:
                if GPIO.input(enviro.water_pump) < 1:
                    water_plants(enviro.water_pump,enviro.air_pump,cycle.duration)
    return 'All Environments Checked'

print(enviro_check())

        