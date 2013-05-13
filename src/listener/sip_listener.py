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
import re




@ListenerFactory.register
class SipListener (AbstractListener, pj.AccountCallback, pj.CallCallback):
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
        time_out = 7,
    )
    
    URI2ID_PATTERN = r'<sip:(.*)@.*>'
    
    
    def __init__(self, *args, **kwargs):
        super(SipListener, self).__init__(*args, **kwargs)
        pj.AccountCallback.__init__(self)
        pj.CallCallback.__init__(self)
        self.msgq = Queue.Queue()
        self.uri2id = re.compile(self.URI2ID_PATTERN)
        
        
    def open(self):
        self.lib = pj.Lib()

        try:
            self.lib.init(log_cfg = pj.LogConfig(level=self.params.loglevel, callback=self.log_cb))
            self.lib.create_transport(pj.TransportType.UDP, pj.TransportConfig())
            self.lib.start()
            
            acc = self.lib.create_account(pj.AccountConfig(
                domain=self.params.domain, 
                username=self.params.username, 
                password=self.params.passwd
            ))
        
            self._set_account(acc)
            self.account.set_callback(self)
            self.registered = threading.Event()
            self.registered.wait()
        
            self.logger.log('sip registration complete, status=%s (%s)' % (self.account.info().reg_status, self.account.info().reg_reason))
            
        except pj.Error, e:
            self.logger.log('PJ error: %s' % e)
            self.lib.destroy()
            self.lib = None
        
        
    def close(self):
        self.lib.destroy()

        
    def on_reg_state(self):
        if self.account.info().reg_status >= 200:
            self.registered.set()


    def on_incoming_call(self, call):
        """Notification about incoming call.

        Unless this callback is implemented, the default behavior is to
        reject the call with default status code.

        Keyword arguments:
        call    -- the new incoming call
        """
        if call == self.call:
            return
        
        ci = call.info()
        self.logger.log('sip: incoming call from %s to %s' % (ci.remote_uri, ci.uri))

        if self.call:
            call.answer(486, 'Busy')
            return
        
        if self.caller(ci.remote_uri) == 'anonymous':
            call.answer(433)
            return

        self._set_call(call)
        
        self.passcode = [ ]

        self.call.set_callback(self)
        self.call.answer(200) # connect
        
        
    def on_time_out(self):
        print 'Time out for call', self.call
        
        if self.call is not None:
            self.lib.thread_register('TimeOut')
            
            self.call.hangup()
            self.time_out = None
            self.logger.log('sip: call time out for %s' % self.caller(self.call.info().remote_uri))

        
    def on_state(self):
        print "Call is ", self.call.info().state_text,
        print "last code =", self.call.info().last_code, 
        print "(" + self.call.info().last_reason + ")"
        
        ci = self.call.info()
        
        if ci.state == pj.CallState.CONFIRMED:
            self.time_out = threading.Timer(self.params.time_out, self.on_time_out)
            self.time_out.start()
        
        if ci.state == pj.CallState.DISCONNECTED:
            msg = '-'.join((self.caller(ci.remote_uri), self.caller(ci.uri), ''.join(self.passcode)))
        
            self.msgq.put(msg)
            self._set_call(None)

            if self.time_out is not None:
                self.time_out.cancel()
                    

    def log_cb(self, level, msg, _len):
        self.logger.log(msg)
        
        
    def caller(self, uri):
        m = self.uri2id.search(uri)
        if m is not None:
            return m.group(1)
    

    def read_id(self):
        msg = self.msgq.get()
            
        return self.KIND, msg


