'''
Created on Mar 17, 2013

@author: ber
'''
import multiprocessing
import time
from listener import ListenerError
from lib.dict_obj import DictObj




class AbstractListener (multiprocessing.Process):
    '''
    An abstract base class for gate listeners
    '''
    name = '*'
        
    DEFAULTS = DictObj(
        block_same = 2,
    )


    def __init__(self, gate, port, queue, params, logger):
        '''
        Constructor
        '''
        super(AbstractListener, self).__init__(name=self.name + '@' + gate)
        self.check_params(params)
        self.gate = gate
        self.port = port
        self.queue = queue
        self.active = True
        self.logger = logger


    def check_params(self, params):
        self.params = DictObj(self.DEFAULTS)
        self.params.update(params)
        
        if None in self.params.itervalues():
            raise ListenerError('Listener type %s@%s is missing required parameters' % (self.name, self.gate))
        
        
    def open(self):
        if self.port:
            self.port.open()


    def close(self):
        if self.port:
            self.port.close()
        
        
    def read_id(self):
        raise NotImplemented()


    def read_msg(self):
        msg_id = self.read_id()
        if msg_id is not None:
            return (self.gate, msg_id)
        else:
            return None


    def run(self):
        last_msg = None
        last_time = time.time()

        self.open()        
        
        while self.active:
            msg = self.read_msg()
            msg_time = time.time()
            
            if msg is not None:
                if last_msg != msg or msg_time - last_time > self.params.block_same:
                    self.queue.put(msg)
                    self.logger.log('Listener %(name)s on %(gate)s: %(msg)s' % 
                        { 'name':self.name, 'gate':self.gate, 'msg':msg }
                    )
                    
                last_msg = msg
                last_time = msg_time

        self.close()
        
            
    def stop(self):
        self.active = False
