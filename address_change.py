import RPi.GPIO as GPIO
#import sensor
import time, qwiic_vl53l1x

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(22, GPIO.OUT)

GPIO.output(17, 0)
GPIO.output(22,0)

GPIO.output(17, 1)

s1 = qwiic_vl53l1x.QwiicVL53L1X()
s1.set_i2c_address(0x40)

GPIO.output(22, 1)

s2 = qwiic_vl53l1x.QwiicVL53L1X()
s2.set_i2c_address(0x20)


#print(sensor.get_distance(s1))
#print(sensor.get_distance(s2))
