from pyo import *
import time

s = Server(duplex=0).boot()

TIMESTAMP = time.time()
LOOPING = False

def looptable_update():
    pass

# For loop pedal sounds
loops = [
    # SndTable(), SndTable(), ... 
]

loop_osc = []

def callback(address, pitch, semitones, volume, sound_id, loop):
    
    duration = time.time()-TIMESTAMP

    if sound_id in synth_tables:
        looper.setPitch(pitch)
        looper.setMul(volume)
        looper.setTable(synth_tables[sound_id])
        if currently_playing[0] not in synth_tables:
            beat.stop()
            looper.out()
    elif sound_id in beat_tables:
        beat_id[0] = sound_id
        beat_pitch[0] = pitch
        note.setValue(60 + semitones)
        if currently_playing[0] not in beat_tables:
            looper.setMul(0)
            beat.play()
    else:
        print('Could not load sound', sound_id)
    currently_playing[0] = sound_id

    if loop and (sound_id in beats_tables or sound_id in synth_tables):
        if not LOOPING:
            loops.append(SndTable(sound_id,start=2,stop=2+duration))
            LOOPING = True
        else:
            loops[-1].append(sound_id,start=2,stop=2+duration)
    else:
        if LOOPING:
            loop_osc.append(Osc(table=loops[-1], freq=loops[-1].getRate())
    
    TIMESTAMP = time.time()
        


rec = OscDataReceive(port=9000, address='/data', function=callback)



# For continuous sounds (synths, leads)
synth_tables = {
    'synth1': SndTable('sounds/synth1.wav'),
    'synth2': SndTable('sounds/synth2.wav'),
}

beat_tables = {
    'kick': SndTable('sounds/kick.wav'),
    'lead': SndTable('sounds/celesta.wav'),
}

looper = Looper(table=synth_tables['synth1'],
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

currently_playing = ['synth']
# ----

# For repeating sounds (kicks, hi-hats, melodies)

note = Sig(60)

beat_id = ['kick']
def _beat_id():
    return beat_id[0]

beat_pitch = [1]
def _beat_pitch():
    return beat_pitch[0]

class Melody(EventInstrument):
    def __init__(self, **args):
        EventInstrument.__init__(self, **args)

        self.filt = Looper(table=beat_tables[_beat_id()],
                           pitch=_beat_pitch(),
                           start=0,
                           mode=0,
                           dur=self.dur,
                           xfade=0,
                           mul=1).out()


beat = Events(instr=Melody,
              midinote=EventSeq([note]),
              beat=EventSeq([1], occurrences=inf), db=0, bpm=140)

# def note_changes():
#     while True:
#         note.setValue(note.value + 1)
#         time.sleep(1)

# import threading
# threading.Thread(target=note_changes).start()


# ----

# For single sounds (808s)
# snd = SndTable('808.wav')
# osc = TableRead(table=snd, freq=snd.getRate()).out()


# ----

s.start()
s.gui(locals())
