import itertools
import sys
import threading
import time

import numpy as np
import pyaudio


VOLUME = 0.5
TONE = 0
RUNNING = True


class Theremin:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.calibration = (5, 10)  # location
        self.sampling_rate = 16000
        self.stream = None

    def play(self):  # 261.6 is middle C
        def tone_gen():
            sample_index = 0
            while RUNNING:
                # sound = np.sin(2 * np.pi * sample_index *
                #                self.get_frequency(TONE) / self.sampling_rate).astype(np.float32)
                f = self.get_frequency(TONE)
                t = sample_index / self.sampling_rate
                sound = (f * t) - np.floor(f * t)
                if int(2 * f * t % 2) == 1:
                    sound = 1 - sound
                sound -= 0.25
                sound *= 4
                sample_index += 1
                yield sound * VOLUME
        tone_generator = tone_gen()

        def callback(in_data, frame_count, time_info, status):
            status = pyaudio.paContinue if RUNNING else pyaudio.paComplete
            data = itertools.islice(tone_generator, frame_count)
            return np.asarray(list(data)).astype(np.float32), status

        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.sampling_rate,
                                  output=True,
                                  stream_callback=callback,
                                  frames_per_buffer=1024)
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
    while RUNNING:
        control = input()
        if control == 'w':
            VOLUME = min(VOLUME + 0.1, 1)
        elif control == 's':
            VOLUME = max(VOLUME - 0.1, 0)
        elif control == 'a':
            TONE -= 1
        elif control == 'd':
            TONE += 1
        elif control == 'q':
            RUNNING = False


if __name__ == '__main__':
    print('''Commands (press enter after entering the command):
    increase volume - w
    decrease volume - s
    increase pitch - a
    decrease pitch - d
    quit - q
    ''')
    theremin = Theremin()
    thread = threading.Thread(target=handle_control)
    thread.daemon = True
    thread.start()
    theremin.play()
    theremin.shutdown()
