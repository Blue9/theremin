from pyo import *

s = Server(duplex=0).boot()


def callback(address, pitch, volume, sound_file):
    looper.setPitch(pitch)
    looper.setMul(volume)
    looper.setTable(tables[sound_file])


rec = OscDataReceive(port=9000, address='/data', function=callback)

# For continuous sounds (synths, leads)
tables = {
    'synth1': SndTable('synth1.wav'),
    'synth2': SndTable('synth2.wav'),
    'bass': SndTable('808.wav')
}
looper = Looper(table=tables['synth1'],
                pitch=1,
                start=2,
                dur=3,
                xfade=67,
                mode=1,
                xfadeshape=1,
                startfromloop=False,
                interp=4,
                autosmooth=True,
                mul=1
                )
stlooper = looper.mix(2).out()

# ----

# For single sounds (808s)
# snd = SndTable('808.wav')
# osc = TableRead(table=snd, freq=snd.getRate()).out()

# ----

# For repeating sounds (kicks, hi-hats, melodies)

# note = Sig(65)
# class Melody(EventInstrument):
#     def __init__(self, **args):
#         EventInstrument.__init__(self, **args)

#         snd = SndTable('celesta.wav')
#         self.filt = Looper(table=snd,
#                            pitch=self.freq / 261.6,
#                            start=0,
#                            mode=0,
#                            dur=self.dur,
#                            xfade=0,
#                            mul=1).out()

# l = Events(instr=Melody,
#            midinote=EventSeq([note]),
#            beat=EventSeq([1], occurrences=inf), db=-20.0, bpm=171)
# l.play()

# def note_changes():
#     while True:
#         note.setValue(note.value + 1)
#         time.sleep(1)

# import threading
# threading.Thread(target=note_changes).start()


# ----

s.start()
s.gui(locals())