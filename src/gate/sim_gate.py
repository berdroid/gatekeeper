'''
Created on Mar 20, 2013

@author: ber
'''


from gate.abstract_gate import AbstractGate
from gate import GateFactory



@GateFactory.register
class SimGate (AbstractGate):
    '''
    simulation of a gate
    '''

    name = 'sim'
    
    def open(self):
        pass


    def close(self):
        pass




