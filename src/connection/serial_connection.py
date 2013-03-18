'''
Created on Mar 18, 2013

@author: ber
'''

from connection import ConnectionFactory
from abstract_connection import AbstractConnection

from serial import Serial, SerialTimeoutException
from lib.dict_obj import DictObj



class SerialConnection (AbstractConnection):
    """
    wrapper around connections using a serial port via pySerial
    """
    name = 'serial'
    description = 'connect via serial port'

        
    DEFAULTS = DictObj(
        device = None,
        baudrate = 9600
    )
    

    def open(self, **kw):
        """
        beginn communication by triggering DTR
        """
        self.port = Serial(self.params.device, self.params.baudrate)
        self.port.timeout = 0.015
        self.port.writeTimeout = 0.25
        self.port.open()

        self.init_string()


    def close(self):
        """
        terminate communication by closing port
        """
        self.port.close()
            

    def write(self, data):
        try:
            self.port.write(data)
        except SerialTimeoutException:
            pass


ConnectionFactory.register(SerialConnection)

