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
        self.pitch_low = 600
        self.pitch_high = 60
        self.vol_low = 60
        self.vol_high = 600
        self.running = True
        self.sound_file = 'synth1'
        self.octave_shift = 0
        self.host = host
        self.bpm= 140
        self.rec = ''
        self._prev_far_limit = True
        self._prev_pitch = 1
        self.repeat = 0
        self.fun_mode = False

    def update(self):
        # pitch, semitones, volume, bpm, sound_file, record_command, server_command, repeat, wobble
        send = OscDataSend(types='fifisssif',
                           port=9000,
                           address='/data',
                           host=self.host)
        while self.running:
            semitones, pitch, far_limit = self.sensor.get_pitch(self)
            if pitch != self._prev_pitch or (self._prev_far_limit and not far_limit):
                play = 'play'
            else:
                play = ''
            self._prev_pitch = pitch
            self._prev_far_limit = far_limit
            os = self.octave_shift
            semitones += os * 12
            volume = self.sensor.get_volume(self)
            pitch *= (2 ** os)
            if self.fun_mode:
                wobble = 1 - volume
                print(wobble, volume)
                volume = 1
            else:
                wobble = 0
            if far_limit:
                volume = 0
            send.send([pitch, semitones, volume, self.bpm, self.sound_file, self.rec, play, self.repeat, wobble])
            self.rec = ''
            time.sleep(0.01)
        send.send([0, 0, 0, 0, '', '', 'stop', 0, 0])

    def set_sound(self, sound):
        self.sound_file = sound
        pass

    def main(self):
        thread = Thread(target=self.update)
        thread.start()
        return thread
