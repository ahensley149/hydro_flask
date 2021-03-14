#!/usr/bin/env python3

import RPi.GPIO as GPIO
import sys

GPIO.setmode(GPIO.BOARD)

lights = int(sys.argv[1])
GPIO.setup(lights, GPIO.OUT)

def lights_on(lights):
  """Turns the lights on

    TODO add a var and split lights to adjust for certain plants only
  """
  GPIO.output(lights, 1)

def lights_off(lights):
  """Turns the lights off
  """
  GPIO.output(lights, 0)

if GPIO.input(lights):
  lights_off(lights)
else:
  lights_on(lights)
