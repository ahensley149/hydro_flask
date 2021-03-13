#!/usr/bin/env python3
import sys
import RPi.GPIO as GPIO
import time

water_pump = (sys.argv[1])
air_pump = 10
duration = sys.argv[2] * 60
GPIO.setmode(GPIO.BOARD)

GPIO.setup(air_pump, GPIO.OUT)
GPIO.setup(water_pump, GPIO.OUT)

GPIO.output(air_pump, 1)
time.sleep(240)
GPIO.output(water_pump, 1)
time.sleep(duration)
GPIO.output(air_pump, 0)
GPIO.output(water_pump, 0)
