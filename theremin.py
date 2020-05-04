import itertools
import sys
import threading
import time

import numpy as np
import pyaudio
import sensor

VOLUME = 0.5
TONE = 0
RUNNING = True


class Theremin:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.calibration = (5, 10)  # location
        self.sampling_rate = 44100
        self.chunk_size = 1024
        self.stream = None

    def play(self):  # 261.6 is middle C
        def tone_gen():
            sample_index = 0
            phase = 0
            while RUNNING:
                f = self.get_frequency(TONE)
                t_start = sample_index * self.chunk_size
                phase_delta = 2 * np.pi * f / self.sampling_rate
                x_vals = np.linspace(phase, phase + phase_delta * self.chunk_size, self.chunk_size, endpoint=False)
                sound = np.sin(x_vals).astype(np.float32)
                phase = (phase + phase_delta * self.chunk_size) % (2 * np.pi)

                # sound = (f * t) - np.floor(f * t)
                # triangle_cutoff = 2 * f * t % 2 >= 1
                # sound[triangle_cutoff] = 1 - sound[triangle_cutoff]
                # sound -= 0.25
                # sound *= 4
                sample_index += 1
                yield sound * VOLUME
        tone_generator = tone_gen()
        
        def callback(in_data, frame_count, time_info, status):
            status = pyaudio.paContinue if RUNNING else pyaudio.paComplete
            data = next(tone_generator)
            return np.asarray(list(data)).astype(np.float32), status

        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.sampling_rate,
                                  output=True,
                                  stream_callback=callback,
                                  frames_per_buffer=self.chunk_size)
        self.stream.start_stream()
        while self.stream.is_active():
            time.sleep(0.1)

    def get_frequency(self, semitones=0, base_note=261.6/2):
        return 2 ** (semitones / 12) * base_note

    def shutdown(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


def handle_control():
    global VOLUME
    global TONE
    global RUNNING
    pitch_control = sensor.get_sensor(0x30)
    volume_control = sensor.get_sensor()
    while RUNNING:
        pitch_distance = sensor.get_distance(pitch_control)
        volume_distance = sensor.get_distance(volume_control)
        if pitch_distance > 300:
            TONE = 0
        elif pitch_distance < 60:
            TONE = 12
        else:
            TONE = int((300 - pitch_distance) / 240 * 12)
        
        if volume_distance > 300:
            VOLUME = 0
        elif volume_distance < 60:
            VOLUME = 1
        else:
            VOLUME = (300 - volume_distance) / 240 

if __name__ == '__main__':
    print('''Commands (press enter after entering the command):
    increase volume - w
    decrease volume - s
    increase pitch - move closer to sensor
    decrease pitch - move farther from sensor
    quit - q
    ''')
    theremin = Theremin()
    thread = threading.Thread(target=handle_control)
    thread.daemon = True
    thread.start()
    theremin.play()
    theremin.shutdown()
