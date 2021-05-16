#!/usr/bin/env python3

import json
import time
from urllib.request import urlopen


min_humid = 50
max_humid = 70

weather_forecast = 'https://api.weather.gov/gridpoints/BOU/58,92/forecast/hourly'

def get_weather_forecast():
    """Retrieves NWS hourly forecast for the location of the grow room
    """
    response = urlopen(weather_forecast)
    data = json.loads(response.read().decode())
    hourly_forecasts = data['properties']['periods']
    forecast_temps = []

    #Get the temperature for the next 10 hours
    for i in range(10):
        forecast_temps.append(hourly_forecasts[i]['temperature'])

    return forecast_temps

def get_temp_limits(outdoor_temp):
    """Set temperature limits based on outside temps and forecasts
    """
    min_temp = 65
    max_temp = 75
    t = time.localtime()
    current_hour = time.strftime("%H", t)
    hour = int(current_hour)
    forecast_temps = get_weather_forecast()

    if hour > 9 and hour < 20:
        if outdoor_temp > 79 or forecast_temps[0] > 79 or forecast_temps[1] > 79 or forecast_temps[2] > 79:            
            max_temp -= 5
            min_temp -= 5
        elif outdoor_temp < 35 or forecast_temps[0] < 35 or forecast_temps[1] < 35 or forecast_temps[2] < 35:            
            min_temp += 2
            max_temp +=5
    elif hour > 5 and hour < 10:
        if forecast_temps[1] > 74 or forecast_temps[2] > 74 or forecast_temps[3] > 79 or forecast_temps[4] > 79:
            max_temp -= 5
            min_temp -= 5
    else:
        if outdoor_temp < 40 or forecast_temps[0] < 40 or forecast_temps[1] < 40 or forecast_temps[2] < 40:
            pass
        elif outdoor_temp > 70 or forecast_temps[0] > 70 or forecast_temps[1] > 70 or forecast_temps[2] > 70:
            max_temp -= 5
            min_temp -=5

    return min_temp, max_temp

def check_air(inside_temp, outdoor_temp, inside_humid, outdoor_humid, min_temp, max_temp):
    """Makes a decision on actions to take depeneding on the temperature and humidity 
      both inside and outside of the grow room
    """
    if inside_temp <= min_temp:
        if outdoor_temp - 15 > inside_temp:
            #Open door and turn on bottom fan
            pass
        else:
            print('Turn on heater')
        if inside_humid <= min_humid:
            print('Turn on humidifier')
    elif inside_temp >= max_temp:
        #Crack door, turn on swamp cooler
        if inside_temp >= max_temp + 2:
            #Turn on upper vent fan
            pass
        if inside_temp >= max_temp + 4:
            #Turn on lower vent fan and cross wind fan
            pass
        if inside_humid <= min_humid:
            #Turn on humidifier
            pass
        if inside_humid >= max_humid:
            #Turn off swamp cooler and humidifier, make sure door is open
            pass
    else:
        if inside_humid <= min_humid:
            print('Turn on humidifier')
        elif inside_humid >= max_humid:
            #Turn off humidifer and or swamp cooler and open door
            print('Open door')
            
