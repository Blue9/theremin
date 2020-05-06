import time
from threading import Thread
from pyo import *
try:
    import sensor
except ModuleNotFoundError:  # Not running on Pi
    import sensor_mock as sensor


class Controller:
    def __init__(self):
        self.s = Server(duplex=0).boot()
        self.s.start()
        self.pitch_low = 300
        self.pitch_high = 60
        self.vol_low = 60
        self.vol_high = 300
        self.running = True
        self.sound_file = 'synth1'
        self.tune = 0.5     # call sensor.tune(self.tune)

    def update_sensors(self):
        send = OscDataSend(types='ffs',  # pitch, volume, sound_file
                           port=9000,
                           address='/data',
                           host='127.0.0.1')
        sensor.get_sensors()
        while self.running:
            pitch = sensor.get_pitch(self)
            volume = sensor.get_volume(self)
            send.send([pitch, volume, self.sound_file])
            time.sleep(0.01)

    def set_sound(self, sound):
        # sound is element of ['synth1', 'synth2', 'bass', 'lead']
        self.sound_file = sound
        pass

    def main(self):
        # TODO in while loop, get sensor value, compute pitch and volume,
        # and send via OSC (add stuff from below to this)
        thread = Thread(target=self.update_sensors)
        thread.start()
        # s.gui(locals())


if __name__ == '__main__':
    s = Server(duplex=0).boot()

    s.start()
    s.gui(locals())
