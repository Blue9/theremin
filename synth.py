from pyo import *

s = Server(duplex=0).boot()
rec = OscReceive(port=9000, address=['/pitch'])
rec.setValue("/pitch", 0.5)

table = SndTable('synth.wav')

looper = Looper(table=table,
                pitch=rec['/pitch'] * 2,
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
s.start()
s.gui(locals())
while True:
    pass
