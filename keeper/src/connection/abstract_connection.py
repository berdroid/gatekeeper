'''
Created on Mar 18, 2013

@author: ber
'''

from connection import ConnectionError
from lib.dict_obj import DictObj



class AbstractConnection (object):
    """
    abstract super class for connection objects
    """
    DEFAULTS = DictObj()
    

    def __init__(self, name, params, logger):
        self.connection_name = name
        self.log = logger
        self.check_params(params)
        
        self.log.log('Connection %s@%s: %s' % (self.name, self.connection_name, self.params))
        
        self.port = None


    def check_params(self, params):
        self.params = DictObj(self.DEFAULTS)
        self.params.update(params)
        
        if None in self.params.itervalues():
            raise ConnectionError('Connection type %s@%s is missing required parameters' % (self.name, self.connection_name))


    def init_string(self):
        try:
            self.write(self.params.init_string)
        except AttributeError:
            pass


    def open(self, **kw):
        raise NotImplementedError('implement the connection methods')


    def close(self):
        raise NotImplementedError('implement the connection methods')


    def read(self):
        return self.port.read(1)


    def write(self, data):
        self.port.write(data)



