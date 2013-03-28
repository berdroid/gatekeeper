'''
Created on Mar 20, 2013

@author: ber
'''
from lib.dict_obj import DictObj
from gate import GateError
import multiprocessing
import time
import atexit



class AbstractGate (multiprocessing.Process):
    '''
    abstract base class for gate controllers
    '''
    name = '*'
    
    DEFAULTS = DictObj(
        hold_time = 1,
        block_time = 10,
    )


    def __init__(self, gate, params, event, logger):
        '''
        Constructor
        '''
        super(AbstractGate, self).__init__(name=self.name + '@' + gate)
        self.gate_name = gate
        self.event = event
        self.log = logger
        self.check_params(params)
        
        self.log.log('Gate %s@%s: %s' % (self.name, self.gate_name, self.params))
        
        self.active = True


    def check_params(self, params):
        self.params = DictObj(self.DEFAULTS)
        self.params.update(params)
        
        if None in self.params.itervalues():
            raise GateError('Connection type %s@%s is missing required parameters' % (self.name, self.gate_name))

        
    def run(self):
        atexit.register(self.on_shutdown, self)
        self.open()
        
        while self.active:
            self.event.wait()

            self.unlock()
            time.sleep(self.params.hold_time)

            self.lock()
            time.sleep(self.params.block_time)
            self.event.clear()
       
        self.close()
        
            
    def stop(self):
        self.active = False
        
        
    def open(self):
        raise NotImplemented()


    def close(self):
        raise NotImplemented()


    def unlock(self):
        self.log.log('Gate %(name)s on %(gate)s: unlocking' % 
            { 'name':self.name, 'gate':self.gate_name, }
        )


    def lock(self):
        self.log.log('Gate %(name)s on %(gate)s: locking' % 
            { 'name':self.name, 'gate':self.gate_name, }
        )
        
        
    def on_shutdown(self):
        self.lock()
        self.close()
        self.log.log('Gate %(name)s on %(gate)s: dhut down' % 
            { 'name':self.name, 'gate':self.gate_name, }
        )




        