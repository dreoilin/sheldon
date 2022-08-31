import logging
import re
import readline
from asyncore import write
from time import sleep

import numpy as np
from serial import Serial


class RAMBo(Serial):
    def __init__(self, port = None, baudrate=250000, timeout=1.0, **kwargs):
        super().__init__(port, baudrate, timeout=timeout, **kwargs)
        logging.info("RAMBo found and and serial connection initiated")
        logging.info("3 second delay for RAMBo startup")
        sleep(3)
        if not self.__startup():
            raise RuntimeError("Could not connect to RAMBo")
        logging.info("Successfully connected")
        # should home x y here
        # self.home()
        # enter z offset here or home manually

    def __startup(self):
        logging.info("Attempting to connect to RAMBo")
        MAX_ATTEMPTS = 3
        for i in range(1,MAX_ATTEMPTS+1):
            logging.info(f"Attempt {i} of {MAX_ATTEMPTS}")
            if self.readline() != "":
                # empty buffer from input
                self.read_buffer()
                return True
        return False

    def readline(self):
        # read ascii only
        return super().readline().decode('ascii')

    def readline_binary(self):
        return super().readline()

    def read_buffer(self):
        buf = ''
        ret = self.readline()
        while ret != '':
            buf += ret
            ret = self.readline()

        return buf

    def read_buffer_binary(self):
        buf = b''
        ret = self.readline_binary()
        while ret != b'':
            buf += ret
            ret = self.readline_binary()
        
        return buf

    def write(self, msg):
        return super().write(msg.encode() + b'\n')

    def write_binary(self, msg):
        return super().write(msg)

    def query(self, msg):
        self.write(msg)
        sleep(1)
        return self.read_buffer()

    def query_binary(self, msg):
        self.write_binary(msg)
        sleep(1)
        return self.read_buffer_binary()

    @property
    def position3d(self):
        ret = self.query("M114")
        ret = dict(re.findall('(\S+):(\S+)', ret)[0:3])
        return np.array([float(ret['X']), float(ret['Y']), float(ret['Z'])])

    @position3d.setter
    def position3d(self, coordinate=np.array([0.0, 0.0, 0.0]), **kwargs):
        # set position
        # case 1: query -> dealt with getter
        # case 2: no change -> query getter and check abs -- would be nice to cache position
        position = self.position3d
        if not (position - coordinate).any():
            logging.debug(f"No change in position from: X->{position[0]}, Y->{position[1]}, Z->{position[2]}")
            return
        
        # case 3: movement
        # move z
        if (position[2] - coordinate[2]):
            logging.debug(f"Adjusting Z height from {position[2]} to {coordinate[2]}")
            self.query(f"G0 F900 Z{coordinate[2]}")
            # await movement complete -> could be implemented as query ?
            self.query("M400")
        
        deltaMax = max((position - coordinate)[0:2])
        
        # set acceleration
        amax = 180
        acc = min(np.rint(amax*deltaMax/5.0), amax)
        self.write(f"M204 T{acc}")
        logging.debug(f"Adjusting acceleration to {acc}")
            
        vmax = 3000 # mm/min
        vel = min(kwargs.get('velocity', vmax), vmax)
        
        self.query(f"G0 F{vel} X{coordinate[0]} Y{coordinate[1]}")
        self.query("M400")
        
        return

    def home(self, **kwargs):
        defaults = {'X' : True, 'Y' : True, 'Z' : False}
        homesets = {k:kwargs.get(k, v) for k,v in defaults.items()}

        for axis,homeset in homesets.items():
            self.query(f"G28 {axis}") if homeset else logging.info(f"Not homing {axis} axis")

