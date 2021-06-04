#!/usr/bin/env python3

import json
import time
import requests
import paho.mqtt.client as mqtt
from urllib import error
from urllib.request import urlopen
from datetime import datetime

weather_forecast = 'https://api.weather.gov/gridpoints/BOU/58,92/forecast/hourly'
weather_station = 'https://swd.weatherflow.com/swd/rest/observations/station/36910?token=ce9d3612-f83c-4aed-a9c2-5ac1f649ea8d'
hygrometer = 'https://api.ubibot.com/channels?account_key=299c02480c6c844d3df27bb6d140d3f7'

now = datetime.now() 
hour = now.strftime("%H")
hour = int(hour)

def get_outdoor_weather():
    """Retrieves weather data from tempest weather station in Backyard
    """
    try:
        response = requests.get(weather_station)
        data = response.json()
        outdoor_temp = (data['obs'][0]['air_temperature'] * 1.8) + 32
        brightness = data['obs'][0]['brightness']
        with open('weather_station.json', 'w') as weather_cache:
            json.dump(data, weather_cache)
    except:
        with open('weather_station.json', 'r') as weather_cache:
            last_weather = json.load(weather_cache)
        weather_time = datetime.fromtimestamp(last_weather['obs'][0]['timestamp'])
        weather_hour = int(weather_time.strftime("%H"))
        if weather_hour == hour:
            outdoor_temp = (last_weather['obs'][0]['air_temperature'] * 1.8) + 32
            brightness = last_weather['obs'][0]['brightness']
        else:
            with open('forecast.json', 'r') as forecast_cache:
                forecast = json.load(forecast_cache)
                for hour_forecast in forecast:
                    if hour == int(hour_forecast['startTime'][11:13]):
                        weather = hour_forecast
                        break
            outdoor_temp = weather['temperature']
            brightness = 50000

    return int(outdoor_temp), brightness

print(get_outdoor_weather())