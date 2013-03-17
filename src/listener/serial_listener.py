'''
Created on Mar 17, 2013

@author: ber
'''


import serial
import time


class SerialListener (object):
    '''
    Common code for listeners on serial interfaces
    '''


    def open_port(self):
        portname, baudrate = self.portname.split(':')
        
        #self.port = serial.Serial(portname, int(baudrate))
        
        self.DATA = 'ABC89'
        self.data = list(self.DATA)
        
        
        
    def read_port(self):
        if len(self.data) == 0:
            self.data = list(self.DATA)
            time.sleep(3)
            
        return self.data.pop()

        return self.port.read()