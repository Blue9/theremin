Run this: python3 theremin.py 

HW Connections:
The SHUT pin on one of the VL53LX sensors is connected to BCM pin 17. This pin is an active low, so when GPIO 17 outputs 0, the connected board powers off. 
In sensor.py, we use this feature to write to a single board and change its address. Then, we set GPIO 17 high and leave that sensor on its original address.

Note: The current implementation will cannot be run multiple times yet without unplugging the sensor's power. This is because the sensors will have their new I2C addresses flashed from the perious time that theremin.py was run. 


