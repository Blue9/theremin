import os
import time
import threading
from pyo import *

s = Server(duplex=0).boot()
s.recordOptions(fileformat=0, sampletype=1)

def callback(address, pitch, semitones, volume, sound_id, record_command):
    """
    OSC callback.

    address is given to us we don't care about it
    pitch is between 0 and 1
    semitones is -24 to 24 (how offset from base note)
    volume is 0 to 1
    sound_id is a string in synth_tables or beat_tables
    record_command is one of empty string, start or reset
    """
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

    if record_command == 'start':
        loop(num_beats=8)
    elif record_command == 'reset':
        loop_play.stop()


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


bpm = 140

beat = Events(instr=Melody,
              midinote=EventSeq([note]),
              beat=EventSeq([1], occurrences=inf), db=0, bpm=bpm)

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

# Loop table


def loop(num_beats=8):
    duration = 60 / bpm * num_beats
    # s.recstart('rec_temp.wav')
    s.recstart()
    print('Started recording!')
    t = threading.Timer(duration, handle_loop, args=(duration,))
    t.start()


def handle_loop(duration):
    print('Stopped recording.')
    s.recstop()
    # os.rename('rec_temp.wav', 'rec.wav')
    # loop_table.setTable(SndTable('rec.wav'))  # reload file
    loop_table.setTable(SndTable(os.path.join(os.path.expanduser('~'), 'pyo_rec.wav')))  # reload file
    loop_table.setDur(duration)
    loop_play.stop()
    loop_play.out()


loop_table = Looper(table=NewTable(1),
                    pitch=1,
                    start=0,
                    mode=1,
                    dur=1,
                    xfade=1,
                    mul=1)

loop_play = loop_table.mix(2)


s.start()
s.gui(locals())
