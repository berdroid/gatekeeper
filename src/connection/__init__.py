
from lib import factory


ConnectionFactory = factory.Factory()

class ConnectionError (Exception):
    pass


import serial_connection
import sim_connection

