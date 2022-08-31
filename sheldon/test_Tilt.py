from drivers import Servo, RAMBo

TILT_SPECS = {
    'PWM_RANGE' : (553, 2270),
    'DEG_PER_USEC' : 0.105,
    'STEP_DIVISOR' : 10000,
    'ROTATION_LIMS' : (-30, 178),
    'DEADBAND_WIDTH' : 8,
    'OFFSET' : 2.0
}


rmbo = RAMBo('/dev/ttyACM0', 250000, timeout=1.0)

tilt = Servo(rmbo, 0, **TILT_SPECS)

import IPython; IPython.embed()
