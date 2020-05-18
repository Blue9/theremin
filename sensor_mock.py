
class Sensor:

    def get_pitch(self, controller):
        return int(controller.pitch_low / controller.pitch_high * 12), controller.pitch_low / controller.pitch_high, False

    def get_volume(self, controller):
        return controller.vol_low / controller.vol_high
