import time
from threading import Thread
from pyo import *
try:
    import sensor
except ModuleNotFoundError:  # Not running on Pi
    print('Using mock sensor')
    import sensor_mock as sensor


class Controller:
    def __init__(self, host='127.0.0.1'):
        self.s = Server(duplex=0).boot()
        self.s.start()
        self.sensor = sensor.Sensor()
        self.base_note = 261.6
        self.pitch_low = 300
        self.pitch_high = 60
        self.vol_low = 60
        self.vol_high = 300
        self.running = True
        self.sound_file = 'synth1'
        self.octave_shift = 0
        self.host = host

    def update(self):
        send = OscDataSend(types='ffs',  # pitch, volume, sound_file
                           port=9000,
                           address='/data',
                           host=self.host)
        while self.running:
            pitch = self.sensor.get_pitch(self) * (2 ** self.octave_shift)
            volume = self.sensor.get_volume(self)
            send.send([pitch, volume, self.sound_file])
            time.sleep(0.01)

    def set_sound(self, sound):
        # sound is element of ['synth1', 'synth2', 'bass', 'lead']
        self.sound_file = sound
        pass

    def main(self):
        thread = Thread(target=self.update)
        thread.start()
        return thread
