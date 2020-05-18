import qwiic_vl53l1x
import time
import RPi.GPIO as GPIO


class Sensor:
    pitch_reset_pin = 22
    vol_reset_pin = 19
    pitch_address = 0x20
    vol_address = 0x30

    def __init__(self, reset=False):
        self.pitch_sensor = None
        self.vol_sensor = None
        self.init_sensors(reset=reset)

    def init_sensors(self, reset=False):
        if reset:
            self.disable_sensors()
            self.enable_sensor(self.pitch_reset_pin)
            self.pitch_sensor = qwiic_vl53l1x.QwiicVL53L1X(address=0x29)
            self.pitch_sensor.set_i2c_address(self.pitch_address)

            self.enable_sensor(self.vol_reset_pin)
            self.vol_sensor = qwiic_vl53l1x.QwiicVL53L1X(address=0x29)
            self.vol_sensor.set_i2c_address(self.vol_address)
        else:
            self.pitch_sensor = qwiic_vl53l1x.QwiicVL53L1X(
                address=self.pitch_address)
            self.vol_sensor = qwiic_vl53l1x.QwiicVL53L1X(
                address=self.vol_address)
        self.setup_sensors()

    @staticmethod
    def disable_sensors():
        GPIO.output(Sensor.pitch_reset_pin, 0)
        GPIO.output(Sensor.vol_reset_pin, 0)

    @staticmethod
    def enable_sensor(pin):
        GPIO.output(pin, 1)

    def setup_sensors(self):
        Sensor._setup_sensor(self.pitch_sensor)
        Sensor._setup_sensor(self.vol_sensor)

    @staticmethod
    def _setup_sensor(sensor):
        sensor.sensor_init()
        sensor.set_distance_mode(2)
        sensor.start_ranging()

    @staticmethod
    def get_factor(semitones):
        return 2 ** (semitones / 12)

    def get_pitch(self, controller):
        pitch_distance = self.pitch_sensor.get_distance()
        low = controller.pitch_low
        high = controller.pitch_high
        if pitch_distance > low:
            return 0, 1
        elif pitch_distance < high:
            return 12, 2
        else:
            semitones = int((low - pitch_distance) / (low - high) * 12)
            return semitones, self.get_factor(semitones)


    def get_volume(self, controller):
        volume_distance = self.vol_sensor.get_distance()
        low = controller.vol_low
        high = controller.vol_high
        if volume_distance > high:
            return 1
        elif volume_distance < low:
            return 0
        else:
            return (volume_distance - low) / (high - low)



GPIO.setmode(GPIO.BCM)
GPIO.setup(Sensor.pitch_reset_pin, GPIO.OUT)
GPIO.setup(Sensor.vol_reset_pin, GPIO.OUT)

if __name__ == '__main__':
    import sys
    if sys.argv[1] == 'reset':
        sensor = Sensor(reset=True)
    else:
        sensor = Sensor()
    while True:
        d = sensor.pitch_sensor.get_distance()
        print(d)

