
from .SCPI.VISA_Instrument import VISA_Instrument
import logging

class VNA(VISA_Instrument):
    def __init__(self, port = None):
        # debug read and write termination 
        # fix usb rules on rpi (??) FUCK
        super().__init__(port=port, read_termination='\n')
        logging.info("Anritsu VNA: Successfully instanciated")

    def connect(self):
        super().connect()
        logging.info("Anritsu VNA: connected")

    # record S parameter
    def record(self):
        pass