def reset_sensor(pin=None):
    pass

def enable_sensor(pin=None):
    pass

def setup_sensors():
    pass

def get_sensors():
    pass

def get_pitch(controller):
    return controller.pitch_low / controller.pitch_high

def get_volume(controller):
    return controller.vol_low / controller.vol_high
