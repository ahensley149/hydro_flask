import serial
import re

uno = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
nano = serial.Serial('/dev/ttyUSB1', 9600, timeout=1)
uno.flush()
nano.flush()

def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

def get_data(sensor):
    data1 = uno.readline().decode('utf-8').rstrip()
    data2 = nano.readline().decode('utf-8').rstrip()
    data1_list = re.split(r"\s", data1)
    data2_list = re.split(r"\s", data2)
    if sensor == 'temp':
        temp = re.split(r"\.", data2_list[5])
        return temp[0]
    if sensor == 'humid':
        humid = re.split(r"\.", data2_list[1])
        return humid[0]
    if sensor == 'ph':
        return data1_list[0]
    if sensor == 'ec':
        return data1_list[1]

def current_ph(ph_sensor):
    if ph_sensor == 1:
        ph_level, _ = get_data('ph')
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
        _, ec_level = get_data('ec')
        if is_number(ec_level):
            return float(ec_level)
        else:
            return 0.0
    elif ec_sensor == 2:
        return 1.5
    else:
        return 0
