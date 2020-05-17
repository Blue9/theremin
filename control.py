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
        self.bpm= 140
        self.rec = ''

    def update(self):
        # pitch, semitones, volume, bpm, sound_file, record_command
        send = OscDataSend(types='fifiss',
                           port=9000,
                           address='/data',
                           host=self.host)
        while self.running:
            semitones, pitch = self.sensor.get_pitch(self)
            os = self.octave_shift
            pitch *= (2 ** os)
            semitones += os * 12
            volume = self.sensor.get_volume(self)
            send.send([pitch, semitones, volume, self.bpm, self.sound_file, self.rec])
            self.rec = ''
            time.sleep(0.01)

    def set_sound(self, sound):
        # sound is element of ['synth1', 'synth2', 'bass', 'lead']
        self.sound_file = sound
        pass

    def main(self):
        thread = Thread(target=self.update)
        thread.start()
        return thread
