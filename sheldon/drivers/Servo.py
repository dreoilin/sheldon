import numpy as np

# might need to move these out of here... ?

TILT_SPECS = {
    'PWM_RANGE' : (553, 2270),
    'DEG_PER_USEC' : 0.105,
    'ROTATION_MAX' : 180,
    'DEADBAND_WIDTH' : 8,
    'OFFSET' : 0.0
}

PAN_SPECS = {
    'PWM_RANGE' : (750, 2250),
    'DEG_PER_USEC' : 0.119,
    'ROTATION_MAX' : 178,
    'DEADBAND_WIDTH' : 2,
    'OFFSET' : 0.0
}

class Servo:
    def __init__(self, rm = None, pin = 'P0', **kwargs):
        self.__rm = rm
        self.__pin = pin
        kwargs =  {k.upper(): v for k, v in kwargs.items()}
        self.__PWM_RANGE = kwargs.get('PWM_RANGE', (0.0, 1.0))
        self.__DEG_PER_USEC = kwargs.get('DEG_PER_USEC', 0.1)
        self.__ROTATION_MAX = kwargs.get('ROTATION_MAX', 90.0)
        self.__DEADBAND_WIDTH_USEC = kwargs.get('DEADBAND_WIDTH', 8)
        self.__OFFSET = kwargs.get('OFFSET', 0.0)

    def _deg2usec(self, deg):

        deg_180 = 90 + deg
        usec_input = min(self.__PWM_RANGE) + np.around(deg_180/self.__DEG_PER_USEC)

        return np.rint(usec_input)

    def _usec2deg(self, usecs):
        
        if usecs == 1:
            deg_p_m_90 = self.__DEG_PER_USEC
        else:
            deg_180 = (usecs-min(self.__PWM_RANGE))*self.__DEG_PER_USEC
        deg_p_m_90 = deg_180-90
    
        return float(deg_p_m_90)

    def write(self, usecs):
        return self.__rm.write(f"M280 {self.__pin} S{usecs}")

    def rotate(self, deg):
        pass

    def reset(self):
        self.__angle = 0.0
        # need to finish this function
        
    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, deg):
        self.__angle = deg