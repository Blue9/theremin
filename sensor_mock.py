
class Sensor:

    def get_pitch(self, controller):
        return 0, controller.pitch_low / controller.pitch_high

    def get_volume(self, controller):
        return controller.vol_low / controller.vol_high
