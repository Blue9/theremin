from pyo import *


class Controller:
    def __init__(self):
        self.pitch_low = 300
        self.pitch_high = 60
        self.vol_low = 60
        self.vol_high = 300

    def main(self):
        # TODO in while loop, get sensor value, compute pitch and volume,
        # and send via OSC (add stuff from below to this)
        pass


if __name__ == '__main__':
    s = Server(duplex=0).boot()

    pitch = Sig(value=0.5)
    pitch.ctrl(title="Pitch")
    send = OscSend(input=[pitch], port=9000,
                address=['/pitch'],
                host='127.0.0.1')

    s.start()
    s.gui(locals())
