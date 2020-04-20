import pyaudio
import numpy as np
import sys
import time


class Theremin:
    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.calibration = (5, 10)  # location
        self.sampling_rate = 16000
        self.stream = self.p.open(format=pyaudio.paFloat32,
                                  channels=1,
                                  rate=self.sampling_rate,
                                  output=True)

    def play(self, frequency=261.6, volume=0.5, duration=5.0):  # 261.6 is middle C
        data = np.arange(self.sampling_rate * duration)
        sound = np.sin(2 * np.pi * data * frequency /
                       self.sampling_rate).astype(np.float32)
        self.stream.write(volume * sound)

    def get_frequency(self, base_note=261.6, semitones=0):
        return 2 ** (semitones / 12) * base_note


    def shutdown(self):
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()


if __name__ == '__main__':
    theremin = Theremin()
    input_data = sys.argv[1:]
    for item in input_data:
        frequency = theremin.get_frequency(semitones=int(item[0]))
        duration = len(item)
        theremin.play(frequency=frequency, duration=duration)
        time.sleep(0.5 * duration)
    theremin.shutdown()
