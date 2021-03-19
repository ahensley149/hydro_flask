import serial
import re

ser = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
nano = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

ph_level = ''
ec_level = ''
i = 0

def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False

def get_data():
    data = ser.readline().decode('utf-8').rstrip()
    data_list = re.split(r"\s", data)
    if is_number(data_list[0]) and is_number(data_list[1]):
        return data_list[0], data_list[1]
    else:
        get_data()

def get_nano_data(sensor):
    data = nano.readline().decode('utf-8').rstrip()
    data_list = re.split(r"\s", data)
    if sensor == 'temp':
        temp = re.split(r"\.", data_list[5])
        return temp[0]
    if sensor == 'humid':
        humid = re.split(r"\.", data_list[1])
        return humid[0]

def current_ph(ph_sensor):
    if ph_sensor == 1:
        ph_level, _ = get_data()
        if is_number(ph_level):
            return float(ph_level)
        else:
            return 0.0
    elif ph_sensor == 2:
        return 5.4
    else:
        return 0

def current_ec(ec_sensor):
    if ec_sensor == 1:
        _, ec_level = get_data()
        if is_number(ec_level):
            return float(ec_level)
        else:
            return 0.0
    elif ec_sensor == 2:
        return 1.5
    else:
        return 0
