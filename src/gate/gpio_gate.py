'''
Created on Mar 25, 2013

@author: ber
'''

from gate.abstract_gate import AbstractGate
from gate import GateFactory
from lib.dict_obj import DictObj



@GateFactory.register
class GpioGate (AbstractGate):
    '''
    GPIO controlled gate
    '''
    DEFAULTS = AbstractGate.DEFAULTS
    
    DEFAULTS.update(DictObj(
        gpio = None,
    ))

    name = 'gpio'
    
    def open(self):
        self.gpio = '/sys/class/gpio/%(gpio)s/' % self.params
        
        with file(self.gpio + 'direction', 'w') as f:
            f.write('out')


    def close(self):
        with file(self.gpio + 'direction', 'w') as f:
            f.write('in')


    def unlock(self):
        super(GpioGate, self).unlock()
        with file(self.gpio + 'value', 'w') as f:
            f.write('1')


    def lock(self):
        super(GpioGate, self).lock()
        with file(self.gpio + 'value', 'w') as f:
            f.write('0')

        
    