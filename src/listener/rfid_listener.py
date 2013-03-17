'''
Created on Mar 17, 2013

@author: ber
'''
from listener.abstract_listener import AbstractListener




class RfidListener (AbstractListener):
    '''
    listener for RFID tags
    '''

    def read_id(self):
        l = [ ]
        for _i in xrange(5):
            l.append(self.read_port())
            
        return 'em4100(' + ''.join(l) + ')'