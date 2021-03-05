"""import serial

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

ph_level = ''
ec_level = ''
i = 0

while True:
    if ser.in_waiting > 0:
        ph_level = ser.readline().decode('utf-8').rstrip()
        ec_level = ser.readline().decode('utf-8').rstrip()
"""
def current_ph(ph_sensor):
    if ph_sensor == 1:
        return 6.0
    elif ph_sensor == 2:
        return 5.4
    else:
        return 0
def current_ec(ec_sensor):
    if ec_sensor == 1:
        return 1.0
    elif ec_sensor == 2:
        return 1.5
    else:
        return 0
