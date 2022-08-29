from serial import Serial
import logging
from time import sleep

class RAMBo(Serial):
    def __init__(self, port = None, baudrate=250000, timeout=1.0, **kwargs):
        super().__init__(port, baudrate, timeout=timeout, **kwargs)
        logging.info("RAMBo found and and serial connection initiated")
        logging.info("10 second delay for RAMBo startup")
        sleep(10)
        if not self.__startup():
            raise RuntimeError("Could not connect to RAMBo")
        logging.info("Successfully connected")

    def __startup(self):
        logging.info("Attempting to connect to RAMBo")
        MAX_ATTEMPTS = 3
        for i in range(1,MAX_ATTEMPTS+1):
            logging.info(f"Attempt {i} of {MAX_ATTEMPTS}")
            if self.readline() != "":
                return True
        return False
        
    def readline(self):
        # read ascii only
        return super().readline().decode('ascii')

    def readline_binary(self):
        return super().readline()

    def write(self, msg):
        return super().write(msg.encode() + b'\n')

    def write_binary(self, msg):
        return super().write(msg)

    @property
    def position3d(self):
        # get and read 3d position of CNC
        pass
    
    @position3d.setter
    def position3d(self, coordinate=(0.0, 0.0, 0.0) ):
        X, Y, Z = coordinate
        # set position
        pass

    def home(self):
        # home axes (currently only X and Y - third endstop?)
        pass

    
    