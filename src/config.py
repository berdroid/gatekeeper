'''
Created on Mar 18, 2013

@author: ber
'''


listeners = [ ]



class ListenerMainGate(object):

    listener_name = 'rfid_serial'
    
    gate_name = 'main_gate'
    
    port_name = '/dev/ttyS0:9600'


listeners.append(ListenerMainGate)



class ListenerBackDoor(object):

    listener_name = 'rfid_serial'
    
    gate_name = 'back_door'
    
    port_name = '/dev/ttyS1:9600'


listeners.append(ListenerBackDoor)
