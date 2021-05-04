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
valve5 = 18
valve6 = 22

GPIO.setup(valve1, GPIO.OUT)
GPIO.output(valve1, 1)
GPIO.setup(valve2, GPIO.OUT)
GPIO.output(valve2, 1)
GPIO.setup(valve3, GPIO.OUT)
GPIO.output(valve3, 1)
GPIO.setup(valve4, GPIO.OUT)
GPIO.output(valve4, 1)
GPIO.setup(valve5, GPIO.OUT)
GPIO.output(valve5, 1)
GPIO.setup(valve6, GPIO.OUT)
GPIO.output(valve6, 1)
GPIO.setup(water_pump, GPIO.OUT)
GPIO.output(water_pump, 1)

print("Enter Valves to Open: ")
valves = input().split()

if '1' in valves:
    GPIO.setup(valve1, GPIO.OUT)
    GPIO.output(valve1, 0)
if '2' in valves:
    GPIO.setup(valve2, GPIO.OUT)
    GPIO.output(valve2, 0)
if '3' in valves:
    GPIO.setup(valve3, GPIO.OUT)
    GPIO.output(valve3, 0)
if '4' in valves:
    GPIO.setup(valve4, GPIO.OUT)
    GPIO.output(valve4, 0)
if '5' in valves:
    GPIO.setup(valve5, GPIO.OUT)
    GPIO.output(valve5, 0)
if '6' in valves:
    GPIO.setup(valve6, GPIO.OUT)
    GPIO.output(valve6, 0)

print("Enter water duration(Minutes): ")
duration = int(input()) * 60
print(duration)

def water_plants(water_pump,valve1,valve2,valve3,valve4,valve5,valve6,duration):

    
    GPIO.output(water_pump, 0)
    time.sleep(duration)
    GPIO.output(valve1, 1)
    GPIO.output(valve2, 1)
    GPIO.output(valve3, 1)
    GPIO.output(valve4, 1)
    GPIO.output(valve5, 1)
    GPIO.output(valve6, 1)
    GPIO.output(water_pump, 1)

water_plants(water_pump,valve1,valve2,valve3,valve4,valve5,valve6,duration)