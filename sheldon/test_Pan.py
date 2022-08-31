from drivers import Servo, RAMBo

PAN_SPECS = {
    'PWM_RANGE' : (750, 2250),
    'DEG_PER_USEC' : 0.119,
    'STEP_DIVISOR' : 100,
    'ROTATION_LIMS' : (-90, 180),
    'DEADBAND_WIDTH' : 2,
    'OFFSET' : 0.0
}

rmbo = RAMBo('/dev/ttyACM0', 250000, timeout=1.0)

pan = Servo(rmbo, 3, **PAN_SPECS)

import IPython; IPython.embed()
