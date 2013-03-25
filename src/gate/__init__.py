

class GateError (Exception):
    pass


from lib import factory
from gate.abstract_gate import AbstractGate



GateFactory = factory.Factory(base=AbstractGate)


import sim_gate
import gpio_gate

