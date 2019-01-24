'''
Created on Mar 17, 2013

@author: ber
'''
from listener import ListenerFactory
import multiprocessing
from lib import logger
import config
from connection import ConnectionFactory
from gate import GateFactory
from auth import AuthorizationFactory, IdentificationFail, AuthorizationFail
import datetime
from Queue import Empty



if __name__ == '__main__':
    gates =  { }
    
    q = multiprocessing.Queue()

    l = logger.SyslogLogger()
    l.open_syslog(**config.Logging.syslog_params)
     
    mail_logger = logger.SyslogMailLogger()
    mail_logger.open_syslog(**config.Logging.syslog_params)
    mail_logger.open_maillog(**config.Logging.mail_params)
    
    process_logger = logger.ProcessLogger()
    process_logger.open_syslog(**config.Logging.syslog_params)
    process_logger.open_processlog(**config.Logging.process_params)

#     l = logger.Logger()
#     mail_logger = l
        
    a = config.Authorization
    auth = AuthorizationFactory(a.auth_type, a.auth_params, l)
    
    for g in config.gates:
        ev = multiprocessing.Event()
        gate = GateFactory(g.gate_type, g.gate_name, g.gate_params, ev, l)
        gates[g.gate_name] = ev
        gate.start()
        
    
    for c in config.listeners:
        if hasattr(c, 'port_type') and c.port_type is not None:
            port = ConnectionFactory(c.port_type, c.gate_name, c.port_params, l)
        else:
            port = None
            
        p = ListenerFactory(c.listener_name, c.gate_name, port, q, c.listener_params, l)
        p.start()

    mail_logger.log('gatekeeper started')

    while True:
        try:
            gate, token_key = q.get(timeout=5)
        
            if token_key is not None:
                authorized, token, person, meta = auth.check(token_key, gate, datetime.datetime.now())
                if authorized:
                    do_mail = meta.maillog

                    if gate in gates:
                        gates[gate].set()
                        
                    mail_logger.log('Authorized: %(name)s'  % person, 'with %(name)s' % token, 'at', gate, do_maillog=do_mail)
                    process_logger.log('Authorized: %(name)s'  % person, 'with %(name)s' % token, 'at', gate, person=person, gate=gate)
                    
        except (IdentificationFail, AuthorizationFail), e:
            mail_logger.log(e.__class__.__name__, str(e))

        except Empty:
            pass
    
            
    