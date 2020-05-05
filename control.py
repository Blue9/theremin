from pyo import *

s = Server(duplex=0).boot()

pitch = Sig(value=0.5)
pitch.ctrl(title="Pitch")
send = OscSend(input=[pitch], port=9000,
               address=['/pitch'],
               host='127.0.0.1')

s.start()
s.gui(locals())
