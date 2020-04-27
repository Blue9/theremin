import qwiic_vl53l1x
import time

def get_sensor(address=None):
    sensor = qwiic_vl53l1x.QwiicVL53L1X(address=address)
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
