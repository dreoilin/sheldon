from time import sleep
import numpy as np

# might need to move these out of here... ?

TILT_SPECS = {
    'PWM_RANGE' : (553, 2270),
    'DEG_PER_USEC' : 0.105,
    'STEP_DIVISOR' : 10000,
    'ROTATION_LIMS' : (-30, 178),
    'DEADBAND_WIDTH' : 8,
    'OFFSET' : 2.0
}

PAN_SPECS = {
    'PWM_RANGE' : (750, 2250),
    'DEG_PER_USEC' : 0.119,
    'STEP_DIVISOR' : 100,
    'ROTATION_LIMS' : (-90, 180),
    'DEADBAND_WIDTH' : 2,
    'OFFSET' : 0.0
}

class Servo:
    def __init__(self, rm = None, pin = 0, **kwargs):
        self.__rm = rm
        self.__pin = pin
        kwargs =  {k.upper(): v for k, v in kwargs.items()}
        self.__PWM_RANGE = kwargs.get('PWM_RANGE', (0.0, 1.0))
        self.__DEG_PER_USEC = kwargs.get('DEG_PER_USEC', 0.1)
        self.__ROTATION_LIMS = kwargs.get('ROTATION_LIMS', (-90, 90.0))
        self.__DEADBAND_WIDTH_USEC = kwargs.get('DEADBAND_WIDTH', 8)
        self.__OFFSET = kwargs.get('OFFSET', 0.0)
        self.__STEP_DIVISOR = kwargs.get('STEP_DIVISOR', 100)
        self.__angle = 0.0

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
        return self.__rm.write(f"M280 P{self.__pin} S{usecs}")

    def __rotate(self, deg):
        offset = self.__OFFSET
        rmin, rmax = self.__ROTATION_LIMS
        if ((rmax - 90 < deg) or (rmin > deg)):
            raise ValueError(f"Error with provided angle: {rmin} < angle < {rmax}")
        else:
            usecs = self._deg2usec(deg+self.__OFFSET)
            delta = abs(self._deg2usec(self.__angle) - usecs)
            steps = np.around(np.linspace(self._deg2usec(self.__angle), usecs, np.rint(float(delta)/self.__STEP_DIVISOR).astype(int)+2))
            for step, input_usecs in enumerate(steps):
                self.write(input_usecs)
                self.angle =input_usecs
                sleep(0.5)

    def reset(self):
        # may need to be class member variable
        reset_angle = self.__OFFSET
        usecs = self._deg2usec(usecs)
        self.write(usecs)

        self.__angle = reset_angle

    # consider replacing with a memoized property with limits    
    @property
    def angle(self):
        # deal with limits here...
        return self.__angle

    @angle.setter
    def angle(self, deg):
        self.__angle = deg
