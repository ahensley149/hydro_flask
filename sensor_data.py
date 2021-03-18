import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
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
    ph_level = ser.readline().decode('utf-8').rstrip()
    ec_level = ser.readline().decode('utf-8').rstrip()
    return ph_level, ec_level

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
        if is_number(ec_level):
            return float(ec_level)
        else:
            return 0.0
    elif ec_sensor == 2:
        return 1.5
    else:
        return 0
