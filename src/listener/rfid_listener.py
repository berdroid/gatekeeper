'''
Created on Mar 17, 2013

@author: ber
'''
from listener.abstract_listener import AbstractListener
from listener import ListenerFactory




class RfidListener (AbstractListener):
    '''
    listener for RFID tags
    '''
    name = 'rfid_em4100'

    NAME = 'em4100'
    SIZE = 5
    

    def read_id(self):
        l = [ ]
        for _i in xrange(self.SIZE):
            l.append('%02x' % ord(self.port.read()))
            
        return self.NAME + '(' + '-'.join(l) + ')'


ListenerFactory.register(RfidListener)

