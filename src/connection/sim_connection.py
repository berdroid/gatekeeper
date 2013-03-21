'''
Created on Mar 18, 2013

@author: ber
'''

from connection import ConnectionFactory
from connection.abstract_connection import AbstractConnection
import time
from lib.dict_obj import DictObj



@ConnectionFactory.register
class SimConnection (AbstractConnection):
    '''
    a simulaton
    '''
    name = 'sim'
    description = 'simulated serial port'

    DEFAULTS = DictObj(
        data = None
    )
    


    def open(self, **kw):
        self.data = list()


    def read(self):
        if len(self.data) == 0:
            self.data = list(self.params.data)
            time.sleep(3)
            
        return chr(self.data.pop(0))



