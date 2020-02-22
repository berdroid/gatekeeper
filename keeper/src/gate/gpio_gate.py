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
    
    
    def gpio_write(self, fn, val):
        with file(self.gpio + fn, 'w') as f:
            f.write(val)

    
    def open(self):
        self.gpio = '/sys/class/gpio/%(gpio)s/' % self.params
        
        self.gpio_write('active_low', '1' if self.params.active_low else '0')
        self.gpio_write('direction', 'out')
        self.gpio_write('value', '0')


    def close(self):
        self.gpio_write('direction', 'in')


    def unlock(self):
        super(GpioGate, self).unlock()
        self.gpio_write('value', '1')


    def lock(self):
        super(GpioGate, self).lock()
        self.gpio_write('value', '0')

        
    