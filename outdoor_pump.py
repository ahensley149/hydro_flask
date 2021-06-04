#!/usr/bin/env python3
#import RPi.GPIO as GPIO
import time
import json
from urllib.request import urlopen
from datetime import datetime

weather_station = 'https://swd.weatherflow.com/swd/rest/observations/station/36910?token=ce9d3612-f83c-4aed-a9c2-5ac1f649ea8d'
now = datetime.now() 
timestamp = now.strftime("%d/%m/%Y %H:%M:%S")

water_pump = 8
valve_1 = 10
valve_2 = 12
valve_3 = 16
valve_4 = 18
valve_5 = 22
valve_6 = 24
extra_relay = 26
duration = 900  # 15 Minutes
#GPIO.setmode(GPIO.BOARD)

def get_outdoor_weather():
    """Retrieves weather data from tempest weather station in Backyard
    """
    response = urlopen(weather_station)
    data = json.loads(response.read().decode())
    outdoor_temp = (data['obs'][0]['air_temperature'] * 1.8) + 32
    today_rain = data['obs'][0]['precip_accum_local_day']
    yesterday_rain = data['obs'][0]['precip_accum_local_yesterday']
    return outdoor_temp, today_rain, yesterday_rain

def check_weather(temp, today_rain, yesterday_rain, duration):
    if today_rain < 1.0 and yesterday_rain < 4.0:
        water_plants(duration)
    elif today_rain < 1.0 and yesterday_rain < 8.0 and temp > 84.9:
        duration -= 300
        water_plants(duration)

def water_plants(duration):
    GPIO.setup(valve_1, GPIO.OUT)
    GPIO.output(valve_1, 0)
    GPIO.setup(valve_2, GPIO.OUT)
    GPIO.output(valve_2, 0)
    GPIO.setup(valve_3, GPIO.OUT)
    GPIO.output(valve_3, 0)
    GPIO.setup(valve_4, GPIO.OUT)
    GPIO.output(valve_4, 0)
    GPIO.setup(water_pump, GPIO.OUT)
    GPIO.output(water_pump, 0)

    time.sleep(duration)

    GPIO.output(water_pump, 1)
    GPIO.output(valve_1, 1)
    GPIO.output(valve_2, 1)
    GPIO.output(valve_3, 1)
    GPIO.output(valve_4, 1)
    
    with open('water_log.json', 'r+') as water_log:
        log = json.load(water_log)
        log[timestamp] = duration/60
        json.dump(log, water_log)
  
    


temp, today_rain, yesterday_rain = get_outdoor_weather()

check_weather(temp, today_rain, yesterday_rain, duration)