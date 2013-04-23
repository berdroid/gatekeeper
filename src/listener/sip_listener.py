'''
Created on Apr 23, 2013

@author: ber
'''
from listener.abstract_listener import AbstractListener
from listener import ListenerFactory
from lib.dict_obj import DictObj
import pjsua as pj
import threading
import Queue



@ListenerFactory.register
class SipListener (AbstractListener, pj.AccountCallback):
    '''
    listener for sip call
    '''
    name = 'sip_call'

    KIND = 'sip'
    
    DEFAULTS = DictObj(AbstractListener.DEFAULTS)
    
    DEFAULTS.update(
        domain = None,
        username = None,
        passwd = None,
        loglevel = 0,
    )
    
    
    def __init__(self, *args, **kwargs):
        super(SipListener, self).__init__(*args, **kwargs)
        self.msgq = Queue.Queue()
        
        
    def open(self):
        self.lib = pj.Lib()

        try:
            self.lib.init(log_cfg = pj.LogConfig(level=self.params.loglevel, callback=self.log_cb))
            self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig())
            self.lib.start()
            
            self.acc = self.lib.create_account(pj.AccountConfig(
                domain=self.params.domain, 
                username=self.params.username, 
                password=self.params.passwd
            ))
        
            self.acc.set_callback(self)
            self.registered = threading.Event()
            self.registered.wait()
        
            self.logger.log('sip registration complete, status=%s (%s)' % (self.acc.info().reg_status, self.acc.info().reg_reason))
            
        except pj.Error, e:
            self.logger.log('PJ error: %s' % e)
            self.lib.destroy()
            self.lib = None
        
        
    def close(self):
        self.lib.destroy()

        
    def on_reg_state(self):
        if self.account.info().reg_status >= 200:
            self.registered.set()

        
    def log_cb(self, level, msg, _len):
        self.logger.log(msg)
    

    def read_id(self):
        msg = self.msgq.get()
            
        return self.KIND + msg


