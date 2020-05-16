from pyo import *

s = Server(duplex=0).boot()


# TODO
# 1. be able to write to sndtable with new sounds
# 2. just add osc? to play new loops in background 
# 3. idk this is kinda hard


s1 = SndTable('synth1.wav')
s2 = SndTable('synth2.wav')
s3 = SndTable('808.wav')

# If we can write the sounds as they're 
# being played we can append like below?
loop = SndTable()
loop.append('synth1.wav')
loop.append('synth2.wav')


osc1 = Osc(table=s1, freq=s1.getRate())
osc2 = Osc(table=s2, freq=s2.getRate())
osc3 = Osc(table=loop, freq=loop.getRate())

# b = FM(carrier=200, ratio=[.5013,.4998], index=6, mul=.2)

# mm.addInput(0, b)
# # mm.addInput(1, tables['synth2'])
import time
from threading import Thread


def secondAudio():
    print("in new thread")
    time.sleep(2)
    osc2.out()



osc3.out()

t = Thread(target=secondAudio)
t.daemon = True
t.start()

s.start()
s.gui(locals())



