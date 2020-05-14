import RPi.GPIO as GPIO
import sensor
import time, qwiic_vl53l1x
from control import Controller

c = Controller()

sensor.get_sensors()

pitch = sensor.get_pitch(c)
volume = sensor.get_volume(c)


while True:
    print(sensor.get_pitch(c))
    print(sensor.get_volume(c))
    time.sleep(2)
