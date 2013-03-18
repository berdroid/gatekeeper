'''
Created on Mar 18, 2013

@author: ber
'''

from connection import ConnectionFactory
from connection.abstract_connection import AbstractConnection
import time



class SimConnection (AbstractConnection):
    '''
    a simulaton
    '''
    name = 'sim'
    description = 'simulated serial port'


    def open(self, **kw):
        self.DATA = [0x06, 0x34, 0x00, 0x45, 0x8e]
        self.data = list(self.DATA)


    def read(self):
        if len(self.data) == 0:
            self.data = list(self.DATA)
            time.sleep(3)
            
        return chr(self.data.pop(0))


ConnectionFactory.register(SimConnection)
