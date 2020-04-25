Run something like this:

python theremin.py


Notes

- Instantiating a PyAudio object using Python2.7 on the Raspberry Pi results in a bunch of warnings  being thrown.
- Right now, the Pi audio output is also REALLY  choppy with noteable drops in audio quality for ~1-2 seconds every ~1-2 seconds. This may have to do with appending a new triangle wave and shifting the phase over to match. 
- Changing pitch also doesn't seem to have an effect right now, but audio is super choppy regardless

- Finally, you have to use apt to install PyAudio and not pip
