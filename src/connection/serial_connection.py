'''
Created on Mar 18, 2013

@author: ber
'''

from connection import ConnectionFactory
from connection.abstract_connection import AbstractConnection

from serial import Serial, SerialTimeoutException
from lib.dict_obj import DictObj



@ConnectionFactory.register
class SerialConnection (AbstractConnection):
    """
    wrapper around connections using a serial port via pySerial
    """
    name = 'serial'
    description = 'connect via serial port'

        
    DEFAULTS = DictObj(AbstractConnection.DEFAULTS)
    
    DEFAULTS.update(
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



if __name__=='__main__':
    import lib.logger
    
    l = lib.logger.Logger()
    
    c = ConnectionFactory('serial', 'gate_1', { 'device':'/dev/ttyAMA0', 'baudrate':9600, }, l)
    c.open()
    
    while True:
        data = c.read()
        if len(data):
            print '%02x' % ord(data)
        
