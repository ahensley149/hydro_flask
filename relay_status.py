import RPi.GPIO as GPIO

GPIO.setup(8, GPIO.OUT)
GPIO.setup(10, GPIO.OUT)
GPIO.setup(12, GPIO.OUT)

if GPIO.input(8) > 0:
    print('Outlet #1 is on')
else:
    print('Outlet #1 is off')

if GPIO.input(10) > 0:
    print('Outlet #2 is on')
else:
    print('Outlet #2 is off')

if GPIO.input(12) > 0:
    print('Outlet #3 is on')
else:
    print('Outlet #3 is off')
