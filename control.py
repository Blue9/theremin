from pyo import *
from threading import Thread
import sensor


class Controller:
    def __init__(self):
        self.pitch_low = 300
        self.pitch_high = 60
        self.vol_low = 60
        self.vol_high = 300
        self.RUNNING = True
    
    def update_sensors(self):
        pitch = Sig(value=0.5)
        volume = Sig(value=0.5)

        send = OscSend(input=[pitch, volume], port=9000,
                    address=['/pitch', '/volume'],
                    host='172.30.9.118')
        sensor.get_sensors()
        import time
        while self.RUNNING:
            pitch.setValue(sensor.get_pitch())
            volume.setValue(sensor.get_volume())
            print(pitch.value, volume.value)
            time.sleep(1)

    def main(self):
        # TODO in while loop, get sensor value, compute pitch and volume,
        # and send via OSC (add stuff from below to this)
        s = Server(duplex=0).boot()
        thread = Thread(target=self.update_sensors())
        
        s.start()
        s.gui(locals())


if __name__ == '__main__':
    s = Server(duplex=0).boot()


    s.start()
    s.gui(locals())
