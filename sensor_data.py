import serial
import re

uno = serial.Serial('/dev/ttyUSB0', 9600, timeout=2)
nano = serial.Serial('/dev/ttyUSB1', 9600, timeout=3)
uno.flush()
nano.flush()

def is_number(values):
    try:
        for value in values:
           float(value)
        return True
    except ValueError:
        return False
    except TypeError:
        return False

def get_data(sensor):
    value_list = ['a']
    num = is_number(value_list)
    while num == False:
        data_uno = uno.readline().decode('utf-8').rstrip()
        data_nano = nano.readline().decode('utf-8').rstrip()
        data_uno_list = re.split(r"\s", data_uno)
        data_nano_list = re.split(r"\s", data_nano)
        try:
            air_temp = re.split(r"\.", data_nano_list[5])
            ph = data_uno_list[0]
            humid = re.split(r"\.", data_nano_list[1])
            ec = data_uno_list[1]
            num = True
        except IndexError:
            value_list = ['a']
            num = False
        if num == True:
            ph = data_uno_list[0]
            ec = data_uno_list[1]
            humid = re.split(r"\.", data_nano_list[1])
            air_temp = re.split(r"\.", data_nano_list[5])
            value_list = [ph, ec, air_temp[0], humid[0]]

    if sensor == 'all':
        all_data = {'ph': ph, 'ec': ec, 'air_temp': air_temp[0], 'humid': humid[0]}
        return all_data
    if sensor == 'air_temp':
        return air_temp[0]
    if sensor == 'humid':
        return humid[0]
    if sensor == 'ph':
        return ph
    if sensor == 'ec':
        return ec

