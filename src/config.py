'''
Created on Mar 18, 2013

@author: ber
'''


listeners = [ ]
gates = [ ]


@listeners.append
class ListenerMainGate (object):

    listener_name = 'rfid_em4100'
    
    gate_name = 'main_gate'
    
    port_type = 'sim'
    port_params = { 'device':'/dev/ttyS0', 'baudrate':9600, 'data':[0x06, 0x34, 0x00, 0x45, 0x8e,  0x06, 0x34, 0x00, 0x67, 0x3c] }



@listeners.append
class ListenerBackDoor (object):

    listener_name = 'rfid_em4100'
    
    gate_name = 'back_door'
    
    port_type = 'sim'
    port_params = { 'data':[0x06, 0x34, 0x00, 0x67, 0x3c] }



class Authorization (object):
    
    auth_type = 'json_file'
    auth_params = { 'json_file': 'auth.json' }


@gates.append
class GateMainGate (object):
    
    gate_type = 'gpio'
    gate_name = 'main_gate'
    gate_params = { 'hold_time': 5, 'gpio': 'gpio2' }


