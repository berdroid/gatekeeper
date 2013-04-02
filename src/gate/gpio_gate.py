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
    DEFAULTS = DictObj(AbstractGate.DEFAULTS)
    
    DEFAULTS.update(
        gpio = None,
        active_low = False,
    )

    name = 'gpio'
    
    def open(self):
        self.gpio = '/sys/class/gpio/%(gpio)s/' % self.params
        
        with file(self.gpio + 'active_low', 'w') as f:
            f.write('1' if self.params.active_low else '0')
        
        with file(self.gpio + 'direction', 'w') as f:
            f.write('out')

        with file(self.gpio + 'value', 'w') as f:
            f.write('0')


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

        
    