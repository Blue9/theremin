import qwiic_vl53l1x
import time
import RPi.GPIO as GPIO

def lock_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, 0)

def unlock_sensor():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(17, GPIO.OUT)
    GPIO.output(17, 1)

def get_sensor(address=None):
    sensor = qwiic_vl53l1x.QwiicVL53L1X()
    if address:
        lock_sensor()
        sensor.set_i2c_address(address)
        time.sleep(0.5)
        unlock_sensor()
    sensor.sensor_init()
    sensor.start_ranging()
    return sensor


def get_distance(sensor):
    #sensor.start_ranging()
    #time.sleep(0.005)
    distance = sensor.get_distance()
    #time.sleep(0.005)
    #sensor.stop_ranging()
    return distance
