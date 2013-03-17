'''
Created on Mar 17, 2013

@author: ber
'''
from listener.abstract_listener import AbstractListener




class RfidListener (AbstractListener):
    '''
    listener for RFID tags
    '''
    NAME = 'em4100'
    SIZE = 5
    

    def read_id(self):
        l = [ ]
        for _i in xrange(self.SIZE):
            l.append('%02x' % ord(self.read_port()))
            
        return self.NAME + '(' + '-'.join(l) + ')'
