import RPi.GPIO as GPIO
import sensor
import time, qwiic_vl53l1x

s1 = sensor.get_sensor(0x30)
s2 = sensor.get_sensor()

print(sensor.get_distance(s1))
print(sensor.get_distance(s2))
