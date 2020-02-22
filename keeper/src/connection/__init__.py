

class ConnectionError (Exception):
    pass


from lib import factory
from connection.abstract_connection import AbstractConnection


ConnectionFactory = factory.Factory(base=AbstractConnection)


import serial_connection
import sim_connection

