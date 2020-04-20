import pyaudio
import numpy as np
import sys

def get_note():
    return int(sys.argv[1])

def get_frequency(tuning=0):
    note = get_note()
    return ((2 ** (1. / 12)) ** (note - 9 + tuning)) * 440

def get_volume():
    return 0.5 if len(sys.argv) < 2 else float(sys.argv[2])

def quit():
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == "__main__":

    frequency = get_frequency()
    volume = get_volume()

    p = pyaudio.PyAudio()
    sampling_rate = 44100
    duration = 1.0

    sound = (np.sin(2*np.pi*np.arange(sampling_rate*duration)*frequency/sampling_rate)).astype(np.float32)
    stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=sampling_rate,
                output=True)

    stream.write(volume * sound)
    
    quit()