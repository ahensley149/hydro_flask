#!/usr/bin/env python3
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

def water_plants(water_pump,air_pump,duration):
    GPIO.setup(air_pump, GPIO.OUT)
    GPIO.setup(water_pump, GPIO.OUT)

    GPIO.output(air_pump, 1)
    time.sleep(240)
    GPIO.output(water_pump, 1)
    time.sleep(duration)
    GPIO.output(air_pump, 0)
    GPIO.output(water_pump, 0)

water_plants(water_pump,air_pump,duration)