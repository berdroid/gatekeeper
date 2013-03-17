'''
Created on Mar 17, 2013

@author: ber
'''
from listener.serial_listener import SerialListener
from listener.rfid_listener import RfidListener
from listener import ListenerFactory



class RfidSerialListener (SerialListener, RfidListener):
    '''
    A gate listener for RFID tag readers on serial ports
    '''
    name = 'rfid_serial'



ListenerFactory.register(RfidSerialListener)