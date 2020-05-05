Install pyo: pip install pyo

Run synth.py in one Terminal tab. This plays audio.

Run control.py in another Terminal tab. This lets you control the pitch.

Change pitch: drag slider.

Change sound: in the window opened by synth.py, click on the interpreter text
box, and enter looper.setTable(SndTable('synth2.wav')) or looper.setTable(SndTable('synth.wav')).


In synth.py there are three types of sounds, continuous, single, and repeating.
Uncomment each one (comment the other two out) and make sure they work. The single sound
does not change pitch (you would have to manually replay the sound with pitch shifted).
The repeating sound does change pitch but not from user input (see note_changes()).

