import qwiic_vl53l1x
import time
import RPi.GPIO as GPIO

ADDR_1 = 17
ADDR_2 = 27
PITCH_SENSOR = None
VOLUME_SENSOR = None
ADDRESS_1 = 0x20
ADDRESS_2 = 0x30
TUNE = 1


GPIO.setmode(GPIO.BCM)
GPIO.setup(ADDR_1, GPIO.OUT)
GPIO.setup(ADDR_2, GPIO.OUT)

def reset_sensor(pin=None):
    if pin:
        GPIO.output(pin, 0)
    else:
        GPIO.output(ADDR_1, 0)
        GPIO.output(ADDR_2, 0)

def enable_sensor(pin=None):
    if pin:
        GPIO.output(pin, 1)
    else:
        GPIO.output(ADDR_1, 1)
        GPIO.output(ADDR_2, 1)

def setup_sensors():
    global PITCH_SENSOR
    global VOLUME_SENSOR
    PITCH_SENSOR.sensor_init()
    VOLUME_SENSOR.sensor_init()
    PITCH_SENSOR.set_distance_mode(1)
    VOLUME_SENSOR.set_distance_mode(1)
    PITCH_SENSOR.start_ranging()
    VOLUME_SENSOR.start_ranging()


def get_sensors():
    global PITCH_SENSOR
    global VOLUME_SENSOR
    reset_sensor()
    
    enable_sensor(ADDR_1)
    PITCH_SENSOR = qwiic_vl53l1x.QwiicVL53L1X(address=0x29)
    PITCH_SENSOR.set_i2c_address(ADDRESS_1)
    
    enable_sensor(ADDR_2) 
    VOLUME_SENSOR = qwiic_vl53l1x.QwiicVL53L1X(address=0x29)
    VOLUME_SENSOR.set_i2c_address(ADDRESS_2)

    setup_sensors()

# t should be a value between 0.1 and 1
def tune(t):
    global TUNE
    TUNE = t

def get_pitch():
    global PITCH_SENSOR
    pitch_distance = PITCH_SENSOR.get_distance()
    if pitch_distance > 600*TUNE:
        return 0
    elif pitch_distance < 60:
        return 12
    else:
        return int((600*TUNE - pitch_distance) / (600*TUNE - 60) * 12)

    return None

def get_volume():
    global VOLUME_SENSOR
    volume_distance = VOLUME_SENSOR.get_distance()
    if volume_distance > 600*TUNE:
        return 0
    elif volume_distance < 60:
        return 1
    else:
        return (600*TUNE - volume_distance) / (600*TUNE - 60)
