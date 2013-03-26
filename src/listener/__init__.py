

class ListenerError (Exception):
    pass
                     

from lib import factory
from listener.abstract_listener import AbstractListener

 
 
ListenerFactory = factory.Factory(base=AbstractListener)


import rfid_listener
