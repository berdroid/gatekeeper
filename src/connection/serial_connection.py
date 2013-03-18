'''
Created on Mar 18, 2013

@author: ber
'''

from connection import ConnectionFactory
from abstract_connection import AbstractConnection

from serial import Serial, SerialTimeoutException



class SerialConnection (AbstractConnection):
    """
    wrapper around connections using a serial port via pySerial
    """
    name = 'serial'
    description = 'connect via serial port'

        
    def open(self, **kw):
        """
        beginn communication by triggering DTR
        """
        try:
            baudrate = self.params.baudrate
            
        except AttributeError:
            baudrate = 9600
            
        self.port = Serial(self.portname, baudrate)
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

