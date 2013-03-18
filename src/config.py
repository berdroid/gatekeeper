'''
Created on Mar 18, 2013

@author: ber
'''


listeners = [ ]



class ListenerMainGate (object):

    listener_name = 'rfid_em4100'
    
    gate_name = 'main_gate'
    
    port_type = 'sim'
    port_params = { 'device':'/dev/ttyS0', 'baudrate':9600, 'data':[0x06, 0x34, 0x00, 0x45, 0x8e] }


listeners.append(ListenerMainGate)



class ListenerBackDoor (object):

    listener_name = 'rfid_em4100'
    
    gate_name = 'back_door'
    
    port_type = 'sim'
    port_params = { 'data':[0x06, 0x34, 0x00, 0x67, 0x3c] }


listeners.append(ListenerBackDoor)
