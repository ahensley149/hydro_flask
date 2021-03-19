import serial
import re

uno = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
nano = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
uno.flush()
nano.flush()

def is_number(values):
    try:
        for value in values:
            float(value)
        return True
    except ValueError:
        return False

def get_data(sensor):
    uno = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    nano = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
    uno.flush()
    nano.flush()
    value_list = ['a']

    while not is_number(value_list):
        data_uno = uno.readline().decode('utf-8').rstrip()
        data_nano = nano.readline().decode('utf-8').rstrip()
        data_uno_list = re.split(r"\s", data_uno)
        data_nano_list = re.split(r"\s", data_nano)
        air_temp = re.split(r"\.", data_nano_list[5])
        humid = re.split(r"\.", data_nano_list[1])
        ph = data_uno_list[0]
        ec = data_uno_list[1]
        value_list = [ph, ec, air_temp, humid]

    if sensor == 'all':
        all_data = {'ph': ph, 'ec': ec, 'air_temp': air_temp, 'humid': humid}
        return all_data
    if sensor == 'air_temp':
        return air_temp[0]
    if sensor == 'humid':
        return humid[0]
    if sensor == 'ph':
        return ph
    if sensor == 'ec':
        return ec

