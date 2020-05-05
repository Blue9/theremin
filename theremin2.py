from array import array
import numpy as np
from time import sleep

import pygame
from pygame.locals import *
from pygame.mixer import Sound, get_init, pre_init


def init(sample_rate):
    pre_init(sample_rate, -16, 1, 1024)


class Note(Sound):
    def __init__(self, frequency, volume=1):
        self.frequency = frequency
        Sound.__init__(self, self.build_samples())
        self.set_volume(volume)

    def build_samples(self):
        period = int(round(get_init()[0] / self.frequency))
        samples = np.zeros(period, dtype=np.int16)
        amplitude = 2 ** (abs(get_init()[1]) - 1) - 1
        for time in range(period):
            samples[time] = (amplitude * np.sin(2 * np.pi * time / period))
            # if time < period / 2:
            #     samples[time] = amplitude
            # else:
            #     samples[time] = -amplitude
        # return np.tile(samples, 512) # get 512 periods at a time
        return samples


def main(in_q, out_q):
    init(96000)
    pygame.mixer.init()
    pygame.init()

    freqs = [261.63, 277.18, 293.66, 311.13, 329.63, 349.23, 369.99, 392.00, 415.30, 440.00, 466.16, 493.88, 523.25]
    # freqs = [261.63, 293.66, 329.63, 349.23, 392.00, 440.00, 493.88, 523.25]
    notes = [Note(f) for f in freqs]
    i = 0
    channel = pygame.mixer.find_channel()
    channel.play(notes[i], fade_ms=100)
    running = True
    while running:
        if not channel.get_busy():
            channel.play(notes[i])
        if not in_q.empty():
            evt = in_q.get()
            if evt == 'quit':
                running = False
            else:
                delta = int(evt)
                i = min(len(notes) - 1, max(0, i + delta))