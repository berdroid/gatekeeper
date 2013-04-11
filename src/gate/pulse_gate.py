'''
Created on Mar 28, 2013

@author: ber
'''
      

from gate.abstract_gate import AbstractGate
from gate import GateFactory
from lib.dict_obj import DictObj
import threading
import time



@GateFactory.register
class PulseGate (AbstractGate):
    '''
    GPIO pulse controlled gate
    '''
    DEFAULTS = DictObj(AbstractGate.DEFAULTS)
    
    DEFAULTS.update(
        gpio = None,
        pulse = 0.010,
    )

    name = 'pulse'
    
    def open(self):
        self.gpio = '/sys/class/gpio/%(gpio)s/' % self.params
        
        with file(self.gpio + 'direction', 'w') as f:
            f.write('out')


    def close(self):
        with file(self.gpio + 'direction', 'w') as f:
            f.write('in')


    def unlock(self):
        super(PulseGate, self).unlock()
        
        self.stop = threading.Event()
        self.runner = threading.Thread(
            target = self.toggle,
            name = 'PulseGate.toggle'
        )
        self.runner.start()


    def lock(self):
        super(PulseGate, self).lock()
        self.stop.set()
        self.runner.join()
        
        with file(self.gpio + 'value', 'w') as f:
            f.write('0')
        
        
    def toggle(self):
        while not self.stop.is_set():
            with file(self.gpio + 'value', 'w') as f:
                f.write('1')
            time.sleep(self.params.pulse)
            with file(self.gpio + 'value', 'w') as f:
                f.write('0')
            time.sleep(self.params.pulse)

        

if __name__=='__main__':
    from lib import logger
    
    l = logger.Logger()
    gate_params = { 'hold_time': 5, 'gpio': 'gpio2', 'active_low': True, 'pulse': 0.01 }
    pg = PulseGate('test', params=gate_params, event=None, logger=l)
    
    pg.open()
    pg.unlock()
    time.sleep(gate_params['hold_time'])
    pg.lock()
    pg.close()
    
    
    
    