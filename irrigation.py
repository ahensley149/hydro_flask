#!/usr/bin/env python3
import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)

water_pump = 24
valve1 = 8
valve2 = 10
valve3 = 12
valve4 = 16
duration = 15 * 60

GPIO.setup(valve1, GPIO.OUT)
GPIO.output(valve1, 1)
GPIO.setup(valve2, GPIO.OUT)
GPIO.output(valve2, 1)
GPIO.setup(valve3, GPIO.OUT)
GPIO.output(valve3, 1)
GPIO.setup(water_pump, GPIO.OUT)
GPIO.output(water_pump, 1)

def water_plants(water_pump,valve1,valve2,valve3,valve4,duration):

    GPIO.output(valve1, 0)
    GPIO.output(valve2, 0)
    GPIO.output(valve3, 0)
    GPIO.output(water_pump, 0)
    time.sleep(duration)
    GPIO.output(valve1, 1)
    GPIO.output(valve2, 1)
    GPIO.output(valve3, 1)
    GPIO.output(water_pump, 1)

water_plants(water_pump,valve1,valve2,valve3,valve4,duration)