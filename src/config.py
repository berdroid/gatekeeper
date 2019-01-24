'''
Created on Mar 18, 2013

@author: ber
'''


listeners = [ ]
gates = [ ]


@listeners.append
class ListenerMainGate (object):

    listener_name = 'rfid_em4100'
    listener_params = { }
    
    gate_name = 'main_gate'
    
    port_type = 'serial'
    port_params = { 'device':'/dev/ttyAMA0', 'baudrate':9600, }


@listeners.append
class ListenerSipMainGate (object):
    
    listener_name = 'sip_call'
    listener_params = { 'domain': '***domain***', 'username': '***user***', 'passwd': '' }
    
    gate_name = 'main_gate'


#@listeners.append
class ListenerBackDoor (object):

    listener_name = 'rfid_em4100'
    listener_params = { }
    
    gate_name = 'back_door'
    
    port_type = 'sim'
    port_params = { 'data':[0x06, 0x34, 0x00, 0x67, 0x3c] }



class Authorization (object):
    
    auth_type = 'json_file'
    auth_params = { 'json_file': 'auth.json' }
    
    
    
class Logging (object):
    
    mail_params = { 'host':'***domain***', 'port':465, 'username':'***user***', 'password':'' }
    syslog_params = { 'ident':'gatekeeper' }
    process_params = { 'script': './handle_gate.sh' }



@gates.append
class GateMainGate (object):
    
    gate_type = 'pulse'
    gate_name = 'main_gate'
    gate_params = { 'hold_time': 5, 'gpio': 'gpio2', 'active_low': True, 'pulse': 0.01 }

