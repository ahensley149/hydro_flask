#!/usr/bin/env python3

import json
import requests
import paho.mqtt.client as mqtt
from urllib.request import urlopen
from datetime import datetime

now = datetime.now() 
timestamp = now.strftime("%d/%m/%Y %H:%M:%S")
hour = now.strftime("%H")
hour = int(hour)	

host = '192.168.86.84'
client = mqtt.Client('door')
client.connect(host)

min_humid = 50
max_humid = 70

weather_forecast = 'https://api.weather.gov/gridpoints/BOU/58,92/forecast/hourly'
weather_station = 'https://swd.weatherflow.com/swd/rest/observations/station/36910?token=ce9d3612-f83c-4aed-a9c2-5ac1f649ea8d'
hygrometer = 'https://api.ubibot.com/channels?account_key=299c02480c6c844d3df27bb6d140d3f7'

def get_weather_forecast():
    """Retrieves NWS hourly forecast for the location of the grow room
    """
    forecast_temps = []
    with open('forecast.json', 'r') as forecast_cache:
        last_forecast = json.load(forecast_cache)
    forecast_time = last_forecast[0]['startTime']
    forecast_hour = int(forecast_time[11:13])
    if forecast_hour == hour:
        hourly_forecasts = last_forecast
    else:
        try:
            response = requests.get(weather_forecast)
            data = response.json()
            hourly_forecasts = data['properties']['periods']
            for i in range(16):
                forecast_time = hourly_forecasts[i]['startTime']
                forecast_hour = int(forecast_time[11:13])
                if forecast_hour < hour:
                    hourly_forecasts[i].pop()

            with open('forecast.json', 'w') as forecast_cache:
                json.dump(hourly_forecasts, forecast_cache)
        except requests.HTTPError:
            last_forecast.pop(0)
            hourly_forecasts = last_forecast
        except KeyError:
            last_forecast.pop(0)
            hourly_forecasts = last_forecast
    
    #Get the temperature for the next 8 hours
    for i in range(8):
        forecast_temps.append(hourly_forecasts[i]['temperature'])

    return forecast_temps

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

def get_hygrometer_reading():
    """Retrieves the Inside temp and humidity from the Ubibot Rest API for the hygrometer in the grow room
    """
    response = urlopen(hygrometer)
    data = json.loads(response.read().decode())
    current = data['channels'][0]['last_values'].split("\"value\":")
    inside_temp = (float(current[1][0:5]) * 1.8) + 32
    inside_humid = int(current[3][0:2])
    return int(inside_temp), inside_humid

def get_temp_limits(outdoor_temp):
    """Set temperature limits based on outside temps and forecasts
    """
    min_temp = 65
    max_temp = 75
    forecast_temps = get_weather_forecast()
    warm_day = False
    print()
    hot_day = False
    cold_day = False
    for forecast_temp in forecast_temps:
        if outdoor_temp > 74 or forecast_temp > 74:
            warm_day = True
            if outdoor_temp > 84 or forecast_temp > 84:
                hot_day = True
        if outdoor_temp <= 35 or forecast_temp <= 35:
            cold_day = True
    print(warm_day)
    if hour > 7 and hour < 19:
        if hot_day and cold_day:            
            max_temp -= 3
            min_temp += 3
        elif warm_day:
            min_temp -= 2
            max_temp -= 2
        elif hot_day:            
            max_temp -= 5
            min_temp -= 5
        elif cold_day:            
            min_temp += 2
            max_temp += 5
    elif hour > 4 and hour < 9:
        if hot_day:
            max_temp -= 5
            min_temp -= 5
        elif warm_day:
            min_temp -= 3
            max_temp -= 3
    else:
        if cold_day:
            min_temp += 3
        elif warm_day:
            min_temp -= 3
            max_temp -= 3
        elif hot_day:
            max_temp -= 5
            min_temp -= 5


    return min_temp, max_temp

def check_air(inside_temp, outdoor_temp, outdoor_brightness, inside_humid, min_temp, max_temp):
    """Makes a decision on actions to take depending on the temperature and humidity 
      both inside and outside of the grow room
    """
    tasks = []
    temp_range = max_temp - min_temp
    
    status_file = open('status.json',)
  
    status = json.load(status_file)
    status_file.close()

    if inside_temp <= min_temp:
        if outdoor_temp - 10 > inside_temp:
            tasks.append('door-3')
            tasks.append('b-fan-on')
        else:
            tasks.append('heater-on')
            tasks.append('door-0')
        if inside_humid <= min_humid:
            tasks.append('cooler-on')
    elif inside_temp >= max_temp:
        if outdoor_brightness < 60000 or hour > 13 or hour < 6:
            tasks.append('door-2')
        else:
            tasks.append('door-1')

        if outdoor_temp >= min_temp - 5:
            tasks.append('cooler-on')
        tasks.append('u-fan-on')
        
        if inside_temp >= max_temp + 1:
            if 'door-1' in tasks:
                    tasks.remove('door-1')
            if 'door-2' in tasks:
                    tasks.remove('door-2')
            if outdoor_brightness < 60000 or hour > 13 or hour < 6:
                tasks.append('door-3')
            else:
                tasks.append('door-2')
            if inside_temp > max_temp + 1:
                tasks.append('b-fan-on')
        else:
            if status['bottom-fan']['status'] == 'on':
                tasks.append('b-fan-off')
                
        if inside_humid <= min_humid:
            tasks.append('cooler-on')
        
        if inside_humid >= max_humid:
            tasks.append('cooler-off')
            tasks.append('door-3')
    elif inside_temp - (temp_range/3) > min_temp and inside_temp + (temp_range/3) < max_temp:
        tasks.append('heater-off')
        tasks.append('b-fan-off')
        tasks.append('u-fan-off')
        if inside_humid <= min_humid:
            tasks.append('cooler-on')
            tasks.append('door-0')
        elif inside_humid >= max_humid:
            tasks.append('cooler-off')
            tasks.append('door-3')
        else:
            tasks.append('cooler-off')
            tasks.append('door-0')
    else:
        if inside_humid <= min_humid:
            tasks.append('cooler-on')
            if status['bottom-fan']['status'] == 'on':
                tasks.append('b-fan-off')
        elif inside_humid >= max_humid:
            #Turn off humidifer and or swamp cooler and open door
            tasks.append('cooler-off')
            tasks.append('door-2')
            if outdoor_temp >= 50 and inside_temp > max_temp - (temp_range / 2):
                tasks.append('u-fan-on')
        elif inside_humid >= min_humid:
            tasks.append('humid-off')
    
    for task in tasks:
        if task == 'cooler-on':
            if status['cooler']['status'] == 'off':
                status['cooler']['status'] = 'on'
                status['cooler']['last-on'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/swamp_cooler_on/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'cooler-off':
            if status['cooler']['status'] == 'on':
                status['cooler']['status'] = 'off'
                status['cooler']['last-off'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/swamp_cooler_off/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'humid-off':
            if status['door']['status'] == 0:
                if status['cooler']['status'] == 'on':
                    status['cooler']['status'] = 'off'
                    status['cooler']['last-off'] = timestamp
                    requests.get(url = "https://maker.ifttt.com/trigger/swamp_cooler_off/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'heater-on':
            if status['heater']['status'] == 'off':
                status['heater']['status'] = 'on'
                status['heater']['last-on'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/heater_on/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'heater-off':
            if status['heater']['status'] == 'on':
                status['heater']['status'] = 'off'
                status['heater']['last-off'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/heater_off/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'b-fan-on':
            if status['bottom-fan']['status'] == 'off':
                status['bottom-fan']['status'] = 'on'
                status['bottom-fan']['last-on'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/bottom_fan_on/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'b-fan-off':
            if status['bottom-fan']['status'] == 'on':
                status['bottom-fan']['status'] = 'off'
                status['bottom-fan']['last-off'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/bottom_fan_off/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'u-fan-on':
            if status['upper-fan']['status'] == 'off':
                status['upper-fan']['status'] = 'on'
                status['upper-fan']['last-on'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/upper_fan_on/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'u-fan-off':
            if status['upper-fan']['status'] == 'on':
                status['upper-fan']['status'] = 'off'
                status['upper-fan']['last-off'] = timestamp
                requests.get(url = "https://maker.ifttt.com/trigger/upper_fan_off/with/key/beLHb8ZjZAJVzHxB1nSatB")
        elif task == 'door-0':
            if status['door']['status'] != 0:
                status['door']['status'] = 0
                status['door']['last-close'] = timestamp
                client.publish("/door/openclose", "0")
        elif task == 'door-1':
            if status['door']['status'] == 0:
                status['door']['status'] = 1
                status['door']['last-open'] = timestamp
                client.publish("/door/openclose", "1")
            elif status['door']['status'] == 2:
                status['door']['status'] = 1
                client.publish("/door/openclose", "-1")
            elif status['door']['status'] == 3:
                status['door']['status'] = 1
                client.publish("/door/openclose", "-2")
            elif status['door']['status'] == 4:
                status['door']['status'] = 1
                client.publish("/door/openclose", "-3")
            elif status['door']['status'] == 5:
                status['door']['status'] = 1
                client.publish("/door/openclose", "-4")
        elif task == 'door-2':
            if status['door']['status'] == 0:
                status['door']['status'] = 2
                status['door']['last-open'] = timestamp
                client.publish("/door/openclose", "2")
            elif status['door']['status'] == 1:
                status['door']['status'] = 2
                client.publish("/door/openclose", "1")
            elif status['door']['status'] == 3:
                status['door']['status'] = 2
                client.publish("/door/openclose", "-1")
            elif status['door']['status'] == 4:
                status['door']['status'] = 2
                client.publish("/door/openclose", "-2")
            elif status['door']['status'] == 5:
                status['door']['status'] = 2
                client.publish("/door/openclose", "-4")     
        elif task == 'door-3':
            if status['door']['status'] == 0:
                status['door']['status'] = 3
                status['door']['last-open'] = timestamp
                client.publish("/door/openclose", "3")
            elif status['door']['status'] == 1:
                status['door']['status'] = 3
                client.publish("/door/openclose", "2")
            elif status['door']['status'] == 2:
                status['door']['status'] = 3
                client.publish("/door/openclose", "1")
            elif status['door']['status'] == 4:
                status['door']['status'] = 3
                client.publish("/door/openclose", "-1")
            elif status['door']['status'] == 5:
                status['door']['status'] = 3
                client.publish("/door/openclose", "-3")
        elif task == 'door-4':
            if status['door']['status'] == 0:
                status['door']['status'] = 4
                status['door']['last-open'] = timestamp
                client.publish("/door/openclose", "4")
            elif status['door']['status'] == 1:
                status['door']['status'] = 4
                client.publish("/door/openclose", "3")
            elif status['door']['status'] == 2:
                status['door']['status'] = 4
                client.publish("/door/openclose", "2")
            elif status['door']['status'] == 3:
                status['door']['status'] = 4
                client.publish("/door/openclose", "1")
            elif status['door']['status'] == 5:
                status['door']['status'] = 4
                client.publish("/door/openclose", "-2")
        elif task == 'door-5':
            if status['door']['status'] < 5:
                status['door']['status'] = 5
                status['door']['last-open'] = timestamp
                client.publish("/door/openclose", "5")
                
    with open('status.json', 'w') as status_file:
        json.dump(status, status_file)
            
forecast = get_weather_forecast()
outdoor_temp, outdoor_brightness = get_outdoor_weather()
min_temp, max_temp = get_temp_limits(outdoor_temp)
inside_temp, inside_humid = get_hygrometer_reading()
check_air(inside_temp, outdoor_temp, outdoor_brightness, inside_humid, min_temp, max_temp)