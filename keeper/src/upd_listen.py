

from listener import ListenerFactory
from lib import logger
import multiprocessing

l = logger.Logger()
l.log('Start')

class ListenerUDP_OTP (object):
    
    listener_name = 'UDP:OTP'
    listener_params = {  }
    
    gate_name = '*'

c = ListenerUDP_OTP()

q = multiprocessing.Queue()

p = ListenerFactory(c.listener_name, c.gate_name, None, q, c.listener_params, l)
p.start()

while True:
    gate, token_key = q.get()
    print(gate, token_key)
