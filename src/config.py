'''
Created on Mar 18, 2013

@author: ber
'''


listeners = [ ]



class ListenerMainGate (object):

    listener_name = 'rfid_em4100'
    
    gate_name = 'main_gate'
    
    port_type = 'sim'
    port_params = { 'device':'/dev/ttyS0', 'baudrate':9600 }


listeners.append(ListenerMainGate)



class ListenerBackDoor (object):

    listener_name = 'rfid_em4100'
    
    gate_name = 'back_door'
    
    port_type = 'sim'
    port_params = { 'device':'/dev/ttyS1', 'baudrate':9600 }


listeners.append(ListenerBackDoor)
