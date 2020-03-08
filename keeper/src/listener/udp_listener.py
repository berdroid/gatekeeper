
'''
Created on Mar 5, 2020

@author: ber
'''
from listener.abstract_listener import AbstractListener
from listener import ListenerFactory
from lib.dict_obj import DictObj
import socket



@ListenerFactory.register
class UDPListener (AbstractListener):
    '''
    listener for RFID tags
    '''
    name = 'udp_otp'

    KIND = 'OTP'
    
    DEFAULTS = DictObj(AbstractListener.DEFAULTS)
    
    DEFAULTS.update(
        addr = '',
        port = 4242,
    )
    
    
    def open(self):
        self.sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_DGRAM
        )
        self.sock.bind((self.params.addr, self.params.port))
        self.logger.log('UDP:OTP started: %s %s' % (self.params.addr, self.params.port))
        
        
    def close(self):
        self.sock.close()
        

    def read_id(self):
        msg, addr = self.sock.recvfrom(256)
        self.logger.log('UDP:OTP %s: %s' % (addr, msg))
        data = msg.split(':')
        
        if len(data) >= 4:
            self.gate = data[0]
            kind = data[1]
            id = data[2]
            hash = data[3]
            
            return kind, '{}:{}'.format(id, hash)
               
        return None
    
